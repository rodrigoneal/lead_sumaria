import PyPDF2

def read_pdf(pdf):
    reader =  PyPDF2.PdfReader(pdf)
    for i in range(len(reader.pages)):
        yield reader.pages[i].extract_text()

