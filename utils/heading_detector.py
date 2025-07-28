from collections import Counter
from utils.classifier_utils import HeadingClassifier
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 42 

clf = HeadingClassifier("models/heading_classifier.pkl")

def determine_heading_levels(pages_data):
    """
    Uses ML + fallback heuristics to detect headings.
    """
    candidates = []
    fallback_candidates = []
    font_sizes = []

    # Collect candidate lines with features
    for page in pages_data:
        for line in page:
            if len(line["text"].strip()) < 3:
                continue
            candidates.append(line)
            font_sizes.append(line["font_size"])
            fallback_candidates.append(line)  # for fallback

    # Predict using trained ML classifier
    predictions = clf.predict(candidates)

    outline = []
    seen = set()
    ml_headings_count = 0

    for line, pred in zip(candidates, predictions):
        if pred in ["Title", "H1", "H2", "H3"]:
            ml_headings_count += 1
            key = (line["text"], line["page"])
            if key not in seen:
                outline.append({
                    "level": pred,
                    "text": line["text"],
                    "page": line["page"]
                })
                seen.add(key)

    # If ML failed (e.g., all predicted 'Other'), use fallback
    if ml_headings_count == 0:
        print("⚠️ ML classifier didn't find headings. Using fallback heuristic.")

        most_common_fonts = [fs for fs, _ in Counter(font_sizes).most_common()]
        heading_fonts = sorted(set(most_common_fonts), reverse=True)[:3]

        font_to_level = {}
        if len(heading_fonts) > 0:
            font_to_level[heading_fonts[0]] = "H1"
        if len(heading_fonts) > 1:
            font_to_level[heading_fonts[1]] = "H2"
        if len(heading_fonts) > 2:
            font_to_level[heading_fonts[2]] = "H3"

        for line in fallback_candidates:
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
    Heuristic filter for heading-like text with multilingual support.
    """
    text = line["text"].strip()

    # 🧩 Existing filters (your current logic)
    if len(text) < 3:
        return False
    if len(text.split()) > 15:
        return False
    if not text[0].isupper():
        return False
    if text.endswith("."):
        return False

    # 🌐 Multilingual compatibility (non-breaking)
    try:
        lang = detect(text)
        unsupported_langs = {"ar", "he"}  # Add more if needed
        if lang in unsupported_langs:
            return False
    except:
        # If language detection fails, fallback to existing logic
        pass

    return True