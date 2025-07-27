import fitz  # PyMuPDF

def extract_text_with_fonts(pdf_path):
    """
    Extract text elements with font sizes and positions per page.
    Returns a list of dicts, one per page.
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
                    line_text += span["text"].strip() + " "
                    font_sizes.append(span["size"])
                if line_text.strip():
                    avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0
                    page_lines.append({
                        "text": line_text.strip(),
                        "font_size": round(avg_font_size, 2),
                        "page": page_num,
                        "bbox": line["bbox"]
                    })
        pages_data.append(page_lines)

    return pages_data