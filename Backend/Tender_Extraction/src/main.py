from pdf_extractor import extract_text
from text_cleaner import clean_text
from pathlib import Path
from clause_detector import detect_clauses

BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "Tendernotice_3.pdf"

pages = extract_text(pdf_path)


for page in pages:
    text = clean_text(page["text"])
    clauses = detect_clauses(text)

    if clauses:
        print(f"\n--- PAGE {page['page']} ---")

        for clause in clauses:
            print(clause)