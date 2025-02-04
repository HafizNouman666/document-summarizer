import PyPDF2

def extract_text_from_pdf(file_stream):
    """Extracts text from a PDF file stream"""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        raise e