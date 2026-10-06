import re


def detect_clauses(text):
    pattern = r'(?m)^\s*(\d+(?:\.\d+)*)[\.\s]+([A-Z][A-Z\s&,-]+)$'

    matches = re.finditer(pattern, text)

    clauses = []

    for match in matches:
        clauses.append({
            "clause": match.group(1),
            "title": match.group(2).strip()
        })

    return clauses