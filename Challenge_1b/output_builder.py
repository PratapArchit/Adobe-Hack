def build_output(documents, persona, job, ranked_sections, ranked_subsections):
    return {
        "metadata": {
            "input_documents": [d["filename"] for d in documents],
            "persona": persona,
            "job_to_be_done": job
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["title"],
                "importance_rank": i + 1,
                "page_number": sec["page"]
            }
            for i, (sec, _) in enumerate(ranked_sections)
        ],
        "subsection_analysis": [
            {
                "document": sub["document"],
                "refined_text": sub["refined"],
                "page_number": sub["page"]
            }
            for sub, _ in ranked_subsections
        ]
    }
