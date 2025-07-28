# Adobe-Hack
This project is part of the Adobe India Hackathon – Connecting the Dots Challenge (Round 1A).
The goal is to extract a structured outline from a PDF, including:
1.TOC-Driven Extraction (Priority)
    a.If a Table of Contents (TOC) is detected, headings are primarily taken from TOC.
    b.Assigns H1/H2 levels based on numbering (e.g., 1. → H1, 2.1 → H2).

2.AI-Based Classification
    For PDFs without TOC, an offline ML model (Logistic Regression) predicts whether a text block is a heading based on:
        a.Font size
        b.Word count
        c.Uppercase ratio
        d.Presence of numbering patterns

3.Heuristic Filtering
    a.Removes:
        Pagination text (e.g., Page 4 of 10)
        Table/form content
        Dates
        Text inside images
    b.Checks:
        Minimum width threshold
        Avoids repetitive decorative text

4.Title Detection
    a.Extracted from the largest text block on the first page.

5.Features
    a.Runs fully offline inside Docker
    b.Processes PDFs under 10 seconds
    c.Handles multilingual PDFs (TOC + AI-based fallback)
    d.Works in CPU-only AMD64 environments



Libraries Used:
1.PyMuPDF (fitz) – PDF text and layout analysis
2.re (Regex) – Pattern matching for structured headings
3.json, os – Output formatting and file handling

Input and Output:
1.Input: Place PDF files inside the input/ folder
2.Output: JSON files will be generated inside the output/ folder with the same name as the PDF

Project Structure:
heading-extractor/
├── Dockerfile
├── requirements.txt
├── extract_outline.py
├── input/      # Place PDF files here
└── output/     # JSON output will be saved here

Build Docker Image
docker build -t heading-extractor .

Running the pdf extractor:
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none heading-extractor

Constraints:
1.Fully offline execution inside Docker
2.Handles PDFs up to 50 pages in under 10 seconds
3.Works in CPU-only AMD64 environments

Author :
Archit and Anagha R Warrier
for Adobe India Hackathon 2025 – Connecting the Dots Challenge.
