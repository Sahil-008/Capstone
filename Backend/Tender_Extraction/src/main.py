from pdf_extractor import extract_text
from text_cleaner import clean_text
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "Tendernotice_3.pdf"

pages = extract_text(pdf_path)

print("Total pages:", len(pages))

for page in pages[:3]:
    cleaned = clean_text(page["text"])

    print(f"\n--- PAGE {page['page']} ---")
    print(cleaned)