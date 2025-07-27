# Adobe-Hack
This project is part of the Adobe India Hackathon – Connecting the Dots Challenge (Round 1A).
The goal is to extract a structured outline from a PDF, including:
1.Document Title
2.Headings (H1, H2, H3) with page numbers

The solution uses font-size and structural analysis to detect headings:
1.Font size-based detection: Largest fonts → H1, next → H2, etc.
2.Regex-based pattern detection: Handles numbered headings like 1., 2.1, 3.2.1.
3.Filtering logic:
    a.Removes form fields, table content, and paragraphs
    b.Ignores text inside images
    c.Applies length and width checks to exclude noise
4.Title detection: Extracted from the largest text block on the first page.
5.Runs offline and processes PDFs in under 10 seconds.

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
