# 🧠 Challenge 1A – Document Outline Extractor

Extract a structured outline (Title, H1, H2, H3) from PDF documents using a **hybrid ML + heuristics model**. Fully offline, CPU-only, and Docker-compatible.

---

## 📁 Project Structure
```
Adobe_Round_1a/
├── input/                          # 📥 Input PDF files
│   ├── file01.pdf
│   └── file02.pdf
├── output/                         # 📤 Output JSON files
│   ├── file01.json
│   └── file02.json
├── models/                         # 🤖 Trained ML model & metadata
│   ├── heading_classifier.pkl
│   ├── label_encoder.pkl
│   └── features_combined.csv       # Optional: for inspection
├── utils/                          # 🔧 Core modules
│   ├── classifier_utils.py         # Loads model & predicts
│   ├── heading_detector.py         # Heading classifier + fallback
│   ├── json_writer.py              # JSON writer
│   └── pdf_parser.py               # Extracts lines & font data
├── sample_dataset/                 # Optional references
│   └── outputs/pdfs/
├── main.py                         # 🚀 Pipeline entry point
├── Dockerfile                      # 📦 CPU-only docker config
├── requirements.txt                # 🧰 Python dependencies
└── README.md                       # 📘 You are here
```
---

## 🐳 🔧 Docker Instructions (IMPORTANT)

### 📦 Step 1: Build the Docker Image

> Ensure you're building for `linux/amd64` to match evaluation environment:

```bash
docker build --platform linux/amd64 -t doc_outline_extractor .
```

⸻

🚀 Step 2: Run the Container

Make sure you have your **input/** and **output/** folders created and PDFs are placed inside input/.
```
Adobe_Round_1a/
├── input/                          # 📥 Input PDF files
│   ├── file01.pdf
│   └── file02.pdf
├── output/                         # 📤 Output JSON files
│   ├── file01.json
│   └── file02.json
├── models/                         # 🤖 Trained ML model & metadata
│   ├── heading_classifier.pkl
│   ├── label_encoder.pkl
│   └── features_combined.csv 
```

```
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  doc_outline_extractor
```
🟢 This will generate one .json per .pdf inside the output/ folder.

⸻

✅ Output Format
```
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

⸻

🧠 Hybrid Heading Detection Approach

This solution combines:
	•	🤖 ML Classifier (RandomForest) trained on layout and text features.
	•	🔠 Font Heuristics for fallback or missing predictions.
	•	🏷️ Title detection via largest font on page 1.

⸻

🎯 Features & Constraint Compliance

Requirement	Status
CPU-only Execution	✅
Offline (No Internet)	✅
Model Size < 200MB	✅ (~100KB)
≤10s per 50-page PDF	✅
JSON Schema Compliance	✅
AMD64 Docker Compatibility	✅


⸻

🧪 ML Model Details
	•	Model: RandomForestClassifier
	•	Training Data: features_combined.csv (text + layout + labels)
	•	Input Features:
	•	Font size
	•	Text length
	•	Bounding box (x0, y0, x1, y1)
	•	Page number
	•	Classes:
	•	Title, H1, H2, H3, Other

⸻

📌 Submission Checklist
	•	✅ Dockerfile in root with platform support
	•	✅ Dependencies containerized
	•	✅ No internet access required
	•	✅ Processes all .pdf files in input/
	•	✅ Outputs .json matching schema
	•	✅ Total runtime < 10s per 50-page PDF

⸻