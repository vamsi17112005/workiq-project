from services.extractors.pdf_extractor import extract_pdf
from services.parsers.markdown_parser import parse_markdown

print("Starting...")

doc = extract_pdf(
    r"C:\Users\vamsi\OneDrive\Desktop\my_intern_placement_prep\ai-search-backend\test_files\offer_letter.pdf"
)

print("PDF extracted")

markdown = doc.export_to_markdown()

print("Markdown length:", len(markdown))

elements = parse_markdown(markdown)

print("Elements count:", len(elements))

for e in elements[:10]:
    print(e)