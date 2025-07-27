from collections import Counter

def get_title(pages_data):
    """
    Extract the document title based on the largest font on page 1.
    """
    if not pages_data or not pages_data[0]:
        return "Untitled"
    first_page = pages_data[0]
    title_candidate = max(first_page, key=lambda x: x["font_size"])
    return title_candidate["text"].strip()

def is_heading_candidate(line):
    """
    Heuristic filter for heading-like text.
    """
    text = line["text"].strip()
    if len(text) < 3:
        return False
    if len(text.split()) > 15:
        return False
    if not text[0].isupper():
        return False
    if text.endswith("."):
        return False
    return True

def determine_heading_levels(pages_data):
    """
    Returns list of structured headings with levels and page numbers.
    """
    candidates = []
    font_sizes = []

    for page in pages_data:
        for line in page:
            if is_heading_candidate(line):
                font_sizes.append(line["font_size"])
                candidates.append(line)

    most_common_fonts = [fs for fs, _ in Counter(font_sizes).most_common()]
    heading_fonts = sorted(set(most_common_fonts), reverse=True)[:3]

    font_to_level = {}
    if len(heading_fonts) > 0:
        font_to_level[heading_fonts[0]] = "H1"
    if len(heading_fonts) > 1:
        font_to_level[heading_fonts[1]] = "H2"
    if len(heading_fonts) > 2:
        font_to_level[heading_fonts[2]] = "H3"

    outline = []
    seen = set()
    for line in candidates:
        level = font_to_level.get(line["font_size"])
        if level:
            key = (line["text"], line["page"])
            if key not in seen:
                outline.append({
                    "level": level,
                    "text": line["text"],
                    "page": line["page"]
                })
                seen.add(key)

    return outline