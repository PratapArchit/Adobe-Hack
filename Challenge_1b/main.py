import json
import os
from pdf_utils import extract_sections_and_subsections
from embedding_utils import load_model, get_embeddings
from ranking import rank_items
from output_builder import build_output
from utils import extract_context, summarize_content

PDF_FOLDER = "pdfs/"

def main(input_path="input.json", output_path="output.json"):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    documents = data["documents"]

    # Extract context from job and persona
    actions, keywords, boost_terms, avoid_terms = extract_context(job, persona)
    print(f"[INFO] Actions: {actions}")
    print(f"[INFO] Keywords: {keywords}")

    all_sections, all_subsections = [], []

    # Extract sections and subsections from PDFs
    for doc in documents:
        file_path = os.path.join(PDF_FOLDER, doc["filename"])
        if not os.path.exists(file_path):
            print(f"[WARNING] Missing file: {file_path}")
            continue
        sections, subsections = extract_sections_and_subsections(file_path)
        all_sections.extend(sections)
        all_subsections.extend(subsections)

    if not all_sections and not all_subsections:
        print("[ERROR] No content extracted.")
        return

    print(f"[INFO] Extracted {len(all_sections)} sections and {len(all_subsections)} subsections.")

    # Load embedding model
    model = load_model()

    # Prepare embeddings
    section_texts = [s["title"] + " " + s["content"] for s in all_sections]
    subsection_texts = [s["title"] + " " + s["content"] for s in all_subsections]

    section_embeddings = get_embeddings(model, section_texts)
    subsection_embeddings = get_embeddings(model, subsection_texts)
    query_embeddings = get_embeddings(model, actions + keywords)

    # Rank sections and subsections separately
    ranked_sections = rank_items(all_sections, section_embeddings, query_embeddings, boost_terms, avoid_terms, job, model)
    ranked_subsections = rank_items(all_subsections, subsection_embeddings, query_embeddings, boost_terms, avoid_terms, job, model)

    # Summarize subsections
    for sub, _ in ranked_subsections:
        sub["refined"] = summarize_content(sub["content"], boost_terms)

    # Build final output
    output = build_output(documents, persona, job, ranked_sections, ranked_subsections)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"[SUCCESS] Output saved to {output_path}")

if __name__ == "__main__":
    main()
