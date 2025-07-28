import fitz  # PyMuPDF

def extract_text_with_fonts(pdf_path):
    """
    Extract text with font sizes and positions from each page of a PDF.
    Returns a list of pages, where each page is a list of dicts:
    {
        "text": "...",
        "font_size": float,
        "page": int,
        "bbox": [x0, y0, x1, y1]
    }
    """
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_lines = []

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                font_sizes = []

                for span in line["spans"]:
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    line_text += text + " "
                    font_sizes.append(span.get("size", 0))

                if line_text.strip():
                    avg_font_size = round(sum(font_sizes) / len(font_sizes), 2) if font_sizes else 0
                    page_lines.append({
                        "text": line_text.strip(),
                        "font_size": round(avg_font_size, 2),
                        "page": page_num,
                        "bbox": line["bbox"],
                        "x0": round(line["bbox"][0], 2),
                        "y0": round(line["bbox"][1], 2),
                        "x1": round(line["bbox"][2], 2),
                        "y1": round(line["bbox"][3], 2)
                    })

        pages_data.append(page_lines)

    return pages_data