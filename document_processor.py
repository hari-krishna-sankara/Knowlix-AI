from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):

    pages = []

    reader = PdfReader(file)

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            pages.append({
                "text": page_text,
                "page": page_number
            })

    return pages


def extract_text_from_docx(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return [{
        "text": text,
        "page": None
    }]


def extract_text_from_txt(file):

    text = file.read().decode("utf-8")

    return [{
        "text": text,
        "page": None
    }]


def extract_text(file):

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    elif file_name.endswith(".txt"):
        return extract_text_from_txt(file)

    else:
        raise ValueError("Unsupported file type")