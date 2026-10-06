import re

def detect_clauses(text):
    pattern = r'(?m)^\s*(\d+(?:\.\d+)*)[\.\s]+(.+)$'

    matches = re.finditer(pattern, text)

    clauses = []

    for match in matches:
        clause_number = match.group(1)
        title = match.group(2).strip()

        # Ignore very short titles
        if len(title) < 5:
            continue

        # Ignore normal sentences
        if not title.isupper():
            continue

        clauses.append({
            "clause": clause_number,
            "title": title
        })

    return clauses