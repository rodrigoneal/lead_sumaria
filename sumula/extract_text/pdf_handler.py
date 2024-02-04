import PyPDF2
import httpx

def read_pdf(pdf):
    reader =  PyPDF2.PdfReader(pdf)
    for i in range(len(reader.pages)):
        yield reader.pages[i].extract_text()

class PDFHandler:
    def __init__(self, pdf):
        self.pdf = pdf
        self.read_pdf = read_pdf
    
class PDFDownloader:
    def __init__(self, ano: str, jogo: str):
        self.url = f"https://conteudo.cbf.com.br/sumulas/{ano}/142{jogo}se.pdf"
    
    async def requisicao(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            return response