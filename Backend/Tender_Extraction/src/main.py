from pathlib import Path

from pdf_extractor import PDFExtractor
from text_cleaner import clean_text
from clause_detector import detect_clauses



BASE_DIR = Path(__file__).resolve().parent.parent


pdf_path = BASE_DIR / "data" / "Tendernotice_3.pdf"


## Step 1: Extract text from PDF
#pages = extract_text(pdf_path)
#
#print("Total pages:", len(pages))
#
#
## Step 2: Detect clauses from each page
#for page in pages:
#    
#    text = clean_text(page["text"])
#
#    clauses = detect_clauses(text)
#
#    for clause in clauses:
#
#        print("\n-----------------------------")
#        print("PAGE:", page["page"])
#        print("CLAUSE:", clause["clause"])
#        print("TITLE:", clause["title"])
#        print("TEXT:")
#        print(clause["text"][:500])







def main():
    extractor = PDFExtractor(pdf_path)

    document = extractor.extract()

    print("File:", document["file_name"])
    print("Total pages:", document["page_count"])

    for page in document["pages"][:3]:

        print("\n" + "=" * 60)
        print("PAGE:", page["page"])
        print("=" * 60)

        print("\nTEXT:")
        print(page["text"][:1000])

        print("\nTEXT BLOCKS:", len(page["blocks"]))
        print("TABLES:", len(page["tables"]))

        for table in page["tables"]:
            print("\nTABLE:", table["table_id"])

            for row in table["rows"]:
                print(row)


if __name__ == "__main__":
    main()