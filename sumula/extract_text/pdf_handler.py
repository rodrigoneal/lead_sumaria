import PyPDF2
import httpx

from sumula.extract_text.extract_text import (
    dados_cronologogia,
    dados_partida,
    dados_arbitragem,
    extrair_relacao_jogadores,
)

from sumula.entities.entities import (
    Jogo,
    Arbitragem,
    Cronologia1T,
    Cronologia2T,
    RelacaoJogadores,
)


class PDFHandler:
    def __init__(self, pdf):
        self.pdf = pdf
        self.read_pdf = self._read_pdf(pdf)

    def _read_pdf(self, pdf):
        return PyPDF2.PdfReader(pdf)

    def pegar_pagina(self, pagina: int):
        return self.read_pdf.pages[pagina].extract_text()

    def extrair_times(self, partida: str):
        self.mandante, self.visitante = partida.split(" X ")

    def primeira_pagina(self, pagina: int):
        text = self.pegar_pagina(pagina)
        partida = dados_partida(text)
        arbitragem = dados_arbitragem(text)
        cronologia = dados_cronologogia(text)
        template = (
            "template_jogadores.json" if len(arbitragem) < 12 else "maior_template.json"
        )
        jogadores = extrair_relacao_jogadores(self.pdf, template)
        _jogo = Jogo(**partida)
        _arbitragem = [Arbitragem(**arbitro) for arbitro in arbitragem]
        cronologia_primeiro = Cronologia1T(
            entrada_mandante=cronologia[0]["Entrada do mandante"],
            atraso_mandante=cronologia[0]["Atraso"],
            entrada_visitante=cronologia[1]["Entrada do visitante"],
            atraso_visitante=cronologia[1]["Atraso"],
            inicio=cronologia[2]["Início 1º Tempo"],
            atraso_inicio=cronologia[2]["Atraso"],
            termino=cronologia[3]["Término do 1º Tempo"],
            acrescimo=cronologia[3]["Acréscimo"],
            resultado=cronologia[-1]["Resultado do 1º Tempo"],
        )
        cronologia_segundo = Cronologia2T(
            entrada_mandante=cronologia[4]["Entrada do mandante"],
            atraso_mandante=cronologia[4]["Atraso"],
            entrada_visitante=cronologia[5]["Entrada do visitante"],
            atraso_visitante=cronologia[5]["Atraso"],
            inicio=cronologia[6]["Início do 2º Tempo"],
            atraso_inicio=cronologia[6]["Atraso"],
            termino=cronologia[7]["Término do 2º Tempo"],
            acrescimo=cronologia[7]["Acréscimo"],
            resultado=cronologia[-1]["Resultado Final"],
        )
        jogadores = [RelacaoJogadores(**jogador) for jogador in jogadores]
        return _jogo, _arbitragem, cronologia_primeiro, jogadores


class PDFDownloader:
    def __init__(self):
        self.url = "https://conteudo.cbf.com.br/sumulas/{ano}/142{jogo}se.pdf"

    def requisicao(self, ano: str, jogo: str):
        with httpx.Client() as client:
            response = client.get(self.url.format(ano=ano, jogo=jogo))
            return response


class Crawler:
    def __init__(self, pdf):
        self.pdf_handler = PDFHandler(pdf)
        self.PDF_downloader = PDFDownloader()

    def pegar_todos_jogos(self):
        anos = ["2022", "2023"]
        jogos = range(1, 375 + 1)
        paginas = range(0, 3)
        for ano in anos:
            for jogo in jogos:
                for pagina in paginas:
                    pdf = self.PDF_downloader.requisicao(ano, jogo)
                    if pdf.status_code == 200:
                        yield self.pdf_handler.pegar_pagina(pagina)
                    else:
                        raise Exception("Erro ao baixar o pdf.")
