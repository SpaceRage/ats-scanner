import PyPDF2

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
