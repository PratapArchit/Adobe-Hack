import os
import json
import fitz
import re
from collections import defaultdict

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

HEADING_REGEX = re.compile(r"^(\d+)(\.\d+)*[.)]?\s+")
DATE_REGEX = re.compile(r"\b\d{1,2}\s+\w+\s+\d{4}\b")
INVALID_PHRASES = ["page", "version", "date", "fig", "table", "%"]
FORM_PHRASES = ["name", "signature", "designation", "rs.", "department", "office", "employee"]

def clean_text(text):
    return ' '.join(text.replace("\n", " ").split())

def extract_title(doc):
    candidates = []
    for block in doc[0].get_text("dict")["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if len(text) > 10:
                    candidates.append((span["size"], text))
    return max(candidates, key=lambda x: x[0])[1] if candidates else "Untitled Document"

def extract_fonts(doc):
    font_counter = defaultdict(int)
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_counter[round(span["size"], 1)] += 1
    return font_counter

def cluster_font_sizes(font_counter):
    sorted_fonts = sorted(font_counter.items(), key=lambda x: (-x[0], -x[1]))
    return [size for size, _ in sorted_fonts[:4]]

def extract_image_areas(page):
    areas = []
    for img in page.get_images(full=True):
        try:
            rect = page.get_image_bbox(img[0])
            areas.append(rect)
        except:
            continue
    return areas

def bbox_overlaps(bbox, areas):
    rect = fitz.Rect(bbox)
    return any(rect.intersects(area) for area in areas)

def extract_headings(doc):
    outline = []
    font_counter = extract_fonts(doc)
    font_sizes = cluster_font_sizes(font_counter)
    for page_num, page in enumerate(doc, start=1):
        image_areas = extract_image_areas(page)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block or "bbox" not in block:
                continue
            if bbox_overlaps(block["bbox"], image_areas):
                continue
            x0, _, x1, _ = block["bbox"]
            if (x1 - x0) < 200:
                continue
            text = ""
            max_font = 0
            for line in block["lines"]:
                for span in line["spans"]:
                    text += " " + span["text"]
                    max_font = max(max_font, round(span["size"], 1))
            text = clean_text(text)
            if len(text) < 4 or not any(c.isalpha() for c in text):
                continue
            if DATE_REGEX.search(text):
                continue
            if any(p in text.lower() for p in FORM_PHRASES + INVALID_PHRASES):
                continue
            if len(text.split()) > 14:
                continue
            if max_font >= font_sizes[0] - 0.5:
                level = "H1"
            elif max_font >= font_sizes[1] - 0.5:
                level = "H2"
            elif max_font >= font_sizes[2] - 0.5:
                level = "H3"
            else:
                if HEADING_REGEX.match(text):
                    depth = text.count(".")
                    if depth == 0:
                        level = "H1"
                    elif depth == 1:
                        level = "H2"
                    else:
                        level = "H3"
                else:
                    continue
            outline.append({"level": level, "text": text, "page": page_num})
    return outline

def process_pdf(input_pdf, output_json):
    doc = fitz.open(input_pdf)
    title = extract_title(doc)
    headings = extract_headings(doc)
    result = {"title": title, "outline": headings}
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.rsplit(".", 1)[0] + ".json")
            print(f"🔍 Processing: {filename}")
            try:
                process_pdf(input_path, output_path)
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
