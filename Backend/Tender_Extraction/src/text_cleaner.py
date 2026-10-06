import re


def clean_text(text):
    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Remove page number at the beginning
    text = re.sub(r"^\s*\d+\s*", "", text)

    return text.strip()