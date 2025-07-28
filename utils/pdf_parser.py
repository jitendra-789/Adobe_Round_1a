import fitz  # PyMuPDF

def extract_text_with_fonts(pdf_path):
    """
    Extract text with font sizes and positions from each page of a PDF.
    Handles multi-column layouts by sorting blocks top-to-bottom, left-to-right.
    Returns a list of pages, where each page is a list of dicts:
    {
        "text": "...",
        "font_size": float,
        "page": int,
        "bbox": [x0, y0, x1, y1],
        "x0": float, "y0": float, "x1": float, "y1": float
    }
    """
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")  # raw block text
        blocks.sort(key=lambda b: (round(b[1], 1), round(b[0], 1)))  # sort by y0, then x0

        page_lines = []
        for block in blocks:
            x0, y0, x1, y1, text, block_no, *_ = block
            if not text.strip():
                continue

            # Optional: fetch font size via detailed dict mode (fallback)
            font_size = 11.0  # default
            spans_blocks = page.get_text("dict")["blocks"]
            for blk in spans_blocks:
                if "lines" not in blk:
                    continue
                for line in blk["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip() in text:
                            font_size = round(span["size"], 2)
                            break

            page_lines.append({
                "text": text.strip(),
                "font_size": font_size,
                "page": page_num,
                "bbox": [x0, y0, x1, y1],
                "x0": round(x0, 2),
                "y0": round(y0, 2),
                "x1": round(x1, 2),
                "y1": round(y1, 2)
            })

        pages_data.append(page_lines)

    return pages_data