from pdf_extractor import extract_text

pdf_path = "data/Tendernotice_3.pdf"

pages = extract_text(pdf_path)

print("Total pages:", len(pages))

for page in pages[:3]:
    print(f"\n--- PAGE {page['page']} ---")
    print(page["text"])