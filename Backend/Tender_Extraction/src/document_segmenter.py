def create_segments(pages):
    segments = []

    for page in pages:
        segments.append({
            "page": page["page"],
            "section": None,
            "clause": None,
            "text": page["text"]
        })

    return segments