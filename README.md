# 📘 Challenge 1A: Understand Your Document

**Adobe India Hackathon 2025 – Round 1A**  
Reimagine the PDF experience by extracting structured outlines like a machine.

---

## 🧠 Problem Statement

Given any PDF (up to 50 pages), the task is to extract:

- `Title` of the document
- `Headings` classified into:
  - H1
  - H2
  - H3

Each heading must include:
- `level`: H1, H2, or H3  
- `text`: heading content  
- `page`: page number where it appears

---

## 📥 Input

All input PDF files are placed in the `/input` directory inside the container.

---

## 📤 Output

For each PDF file, a corresponding `.json` file will be saved to `/output`.  
Output format:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 🧰 Tech Stack

- Python 3.10  
- PyMuPDF (`fitz`) for PDF parsing  
- Heuristic-based logic for heading classification  
- Docker (CPU-only, AMD64)

---

## 🚀 How to Build and Run

### 📦 Build the Docker image

```bash
docker build --platform linux/amd64 -t pdf-processor .
```

### ▶️ Run the container

```bash
docker run --rm \
  --platform linux/amd64 \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

---

## 🧠 Approach Summary

1. **PDF Parsing**  
   Extracts all lines with font size, position, and text per page using PyMuPDF.

2. **Title Detection**  
   Largest text on the first page is selected as the title.

3. **Heading Detection**  
   Headings are filtered using:
   - Font size hierarchy  
   - Capitalization  
   - Punctuation rules (no periods)  
   - Line length (shorter = more likely a heading)  
   - Deduplication

4. **Outline Output**  
   Results are saved to a structured JSON with proper heading levels.

---

## 📁 Folder Structure

```
Challenge_1a/
├── input/                 # PDF input folder
├── output/                # Output JSONs (git-ignored)
├── utils/                 # PDF parsing and heading logic
│   ├── pdf_parser.py
│   └── heading_detector.py
├── Dockerfile             # Container setup
├── main.py                # Entrypoint script
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignore venv, output, etc.
└── README.md              # This file
```

---

## ✅ Constraints Met

- ✅ Platform: `linux/amd64`  
- ✅ CPU-only, offline execution  
- ✅ Model-free (≤200MB)  
- ✅ Sub-10s execution on 50-page PDFs  
- ✅ Robust heuristics (not font-size only)

---

## 👨‍💻 Author

**Jitendra Kolli**  
Adobe Hackathon 2025 Participant  
[https://github.com/jitendra-789](https://github.com/jitendra-789)

---

## 🔒 Note

This repository is kept private until the hackathon deadline, as per the instructions.