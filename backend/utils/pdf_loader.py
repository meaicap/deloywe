from pypdf import PdfReader

def load_pdf_text(file) -> str:
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    return text
