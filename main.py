import os
import json
from utils.pdf_parser import extract_text_with_fonts
from utils.heading_detector import get_title, determine_heading_levels

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_pdf_file(pdf_filename):
    pdf_path = os.path.join(INPUT_DIR, pdf_filename)
    parsed_pages = extract_text_with_fonts(pdf_path)

    title = get_title(parsed_pages)
    outline = determine_heading_levels(parsed_pages)

    output_data = {
        "title": title,
        "outline": outline
    }

    output_filename = pdf_filename.replace(".pdf", ".json")
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(output_path, "w") as out_file:
        json.dump(output_data, out_file, indent=2)
    
    print(f"✅ Processed {pdf_filename} → {output_filename}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            process_pdf_file(filename)

if __name__ == "__main__":
    main()