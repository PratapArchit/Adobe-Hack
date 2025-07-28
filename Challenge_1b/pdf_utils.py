import fitz
import os
import re
from utils import normalize_text
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

GENERIC_HEADINGS = {"introduction", "summary", "overview", "conclusion", "abstract", "notes"}

def generate_title(heading, content, previous_main_heading=None):
    heading_clean = heading.lower().strip()
    if heading_clean in GENERIC_HEADINGS:
        if previous_main_heading:
            return f"{previous_main_heading} - {heading.title()}"
        else:
            # Extract keywords for fallback
            words = [w for w in re.findall(r'\b[a-zA-Z]+\b', content.lower()) if w not in stop_words]
            freq = nltk.FreqDist(words)
            top_keywords = [word for word, _ in freq.most_common(2)]
            keywords_str = ", ".join(top_keywords) if top_keywords else ""
            return f"{heading.title()}: {keywords_str}"
    return heading.strip()

def extract_sections_and_subsections(pdf_path):
    doc = fitz.open(pdf_path)
    sections, subsections = [], []
    previous_main_heading = None

    for page_num, page in enumerate(doc, start=1):
        blocks = [normalize_text(b[4]) for b in page.get_text("blocks") if b[4].strip()]

        current_section = None
        section_content = []

        for block in blocks:
            if is_section_heading(block):
                if current_section and section_content:
                    title = generate_title(clean_title(current_section), " ".join(section_content), previous_main_heading)
                    sections.append({
                        "title": title,
                        "content": " ".join(section_content).strip(),
                        "document": os.path.basename(pdf_path),
                        "page": page_num
                    })
                    subsections.extend(split_into_subsections(title, section_content, pdf_path, page_num))

                if clean_title(block).lower() not in GENERIC_HEADINGS:
                    previous_main_heading = clean_title(block)

                current_section = block
                section_content = []
            else:
                section_content.append(block)

        if current_section and section_content:
            title = generate_title(clean_title(current_section), " ".join(section_content), previous_main_heading)
            sections.append({
                "title": title,
                "content": " ".join(section_content).strip(),
                "document": os.path.basename(pdf_path),
                "page": page_num
            })
            subsections.extend(split_into_subsections(title, section_content, pdf_path, page_num))

    return sections, subsections

def clean_title(text):
    title = re.sub(r"\s*\n\s*", " ", text.strip())
    return title

def is_section_heading(text):
    if not text:
        return False
    words = text.split()
    return (
        len(words) <= 12 and
        text.count('.') <= 1 and
        (text[0].isupper() or text.isupper())
    )

def split_into_subsections(title, content_lines, pdf_name, page_num):
    subsections = []
    for line in content_lines:
        if len(line.split()) >= 4:
            subsections.append({
                "title": title,
                "content": normalize_text(line),
                "document": os.path.basename(pdf_name),
                "page": page_num
            })
    return subsections
