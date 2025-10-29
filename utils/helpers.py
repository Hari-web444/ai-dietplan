import re

def parse_quantity(text: str):
    # Very simple parser: converts "200 g", "200g", "2 pieces", "1 cup" to grams or counts
    text = text.lower().strip()
    m = re.search(r"(\d+\.?\d*)\s*(g|grams|gm)\b", text)
    if m:
        return float(m.group(1)), "g"
    m = re.search(r"(\d+)\s*(pieces|pcs|piece)\b", text)
    if m:
        return int(m.group(1)), "pieces"
    m = re.search(r"(\d+\.?\d*)\s*(cup|cups)\b", text)
    if m:
        return float(m.group(1)), "cup"
    # fallback: try to parse number
    m = re.search(r"(\d+\.?\d*)", text)
    if m:
        return float(m.group(1)), "unit"
    return None, None
