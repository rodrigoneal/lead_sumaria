from tempfile import NamedTemporaryFile, TemporaryFile
import PyPDF2
import httpx

from sumula.extract_text.extract_text import (
    dados_acrescimos,
    dados_cartao_amarelo,
    dados_cartao_vermelho,
    dados_comissao_tecnica,
    dados_cronologogia,
    dados_jogo_numero,
    dados_observacoes_eventuais,
    dados_ocorrencias,
    dados_partida,
    dados_arbitragem,
    dados_relatorio_assistente,
    dados_substituicao,
    extrair_relacao_jogadores,
    dados_gols,
)

from sumula.entities.entities import (
    Acrescimo,
    Assistente,
    CartaoVermelho,
    CartoesAmarelo,
    Comissao,
    ComissaoTecnica,
    EquipeComissao,
    Escalacao,
    Gols,
    Jogo,
    Arbitragem,
    Cronologia1T,
    Cronologia2T,
    Observacoes,
    Ocorrencias,
    RelacaoJogadores,
    Equipe,
    PrimeiraPagina,
    Cronologia,
    SegundaPagina,
    Substituicoes,
    Sumula,
    TerceiraPagina,
)


class PDFHandler:
    def __init__(self, pdf):
        self.pdf = pdf
        self.read_pdf = self._read_pdf(pdf)
        self.mandante, self.visitante = self.dados_jogo(self.pegar_pagina(0))

    def dados_jogo(self, texto):
        dados = dados_partida(texto)
        mandante = dados["mandante"]
        visitante = dados["visitante"]
        return mandante, visitante

    def _read_pdf(self, pdf):
        return PyPDF2.PdfReader(pdf)

    def pegar_pagina(self, pagina: int):
        return self.read_pdf.pages[pagina].extract_text()

    def primeira_pagina(self):
        text = self.pegar_pagina(0)
        partida = dados_partida(text)
        jogo_num = dados_jogo_numero(text)
        arbitragem = dados_arbitragem(text)
        cronologia = dados_cronologogia(text)
        template = (
            "template_jogadores.json" if len(arbitragem) < 12 else "maior_template.json"
        )
        jogadores = extrair_relacao_jogadores(self.pdf, template)
        _jogo = Jogo(**partida, jogo_num=jogo_num)
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
        times = []
        for jogador in jogadores:
            _temp = []
            for escalacao in jogador["escalacao"]:
                relacao = RelacaoJogadores(
                    numero=escalacao["No"],
                    apelido=escalacao["Apelido"],
                    nome=escalacao["Nome Completo"],
                    t_r=escalacao["T/R"],
                    p_a=escalacao["P/A"],
                    cbf=escalacao["CBF"],
                )
                _temp.append(relacao)
            times.append(Equipe(time=jogador["time"], escalao=_temp))
        escalacao = Escalacao(mandante=times[0], visitante=times[1])
        cronologia = Cronologia(
            primeiro_tempo=cronologia_primeiro, segundo_tempo=cronologia_segundo
        )
        return PrimeiraPagina(
            jogo=_jogo,
            arbitragem=_arbitragem,
            cronologia=cronologia,
            escalacao=escalacao,
        )

    def segunda_pagina(self):
        text = self.pegar_pagina(1)
        if not self.mandante or not self.visitante:
            self.extrair_times(text)
        comissoes = dados_comissao_tecnica(text, self.mandante, self.visitante)
        equipes_comissao = []
        for k, v in comissoes.items():
            _temp = []
            for i in v:
                _temp.append(ComissaoTecnica(**i))
            equipes_comissao.append(EquipeComissao(time=k, comissao=_temp))
        comissao = Comissao(mandante=equipes_comissao[0], visitante=equipes_comissao[1])
        _gols = dados_gols(text)
        gols = [Gols(**gol) for gol in _gols]
        cartoes = dados_cartao_amarelo(text)
        cartao_amarelo = [CartoesAmarelo(**cartao) for cartao in cartoes]
        vermelhos = dados_cartao_vermelho(text)
        cartao_vermelho = [CartaoVermelho(**cartao) for cartao in vermelhos]
        return SegundaPagina(
            comissao=comissao,
            gols=gols,
            cartoes_amarelo=cartao_amarelo,
            cartoes_vermelho=cartao_vermelho,
        )

    def terceira_pagina(self):
        text = self.pegar_pagina(2)
        _ocorrencias = dados_ocorrencias(text)
        _acrescimos = dados_acrescimos(text)
        _observacoes = dados_observacoes_eventuais(text)
        _assistente = dados_relatorio_assistente(text)
        _substituicao = dados_substituicao(self.pdf)
        ocorrencias = Ocorrencias(mensagem=_ocorrencias)
        acrescimos = Acrescimo(mensagem=_acrescimos)
        observacao = Observacoes(mensagem=_observacoes)
        assistente = Assistente(mensagem=_assistente)
        substituicao = [Substituicoes(**i) for i in _substituicao]

        return TerceiraPagina(
            ocorrencias=ocorrencias,
            acrescimos=acrescimos,
            observacao=observacao,
            assistente=assistente,
            substituicao=substituicao,
        )

    def sumula(self):
        # if len(self.read_pdf.pages) > 3:
        #     raise Exception("PDF com mais de 3 paginas")
        return Sumula(
            primeira_pagina=self.primeira_pagina(),
            segunda_pagina=self.segunda_pagina(),
            terceira_pagina=self.terceira_pagina(),
        )

class PDFDownloader:
    def __init__(self):
        self.url = "https://conteudo.cbf.com.br/sumulas/{ano}/142{jogo}se.pdf"

    def requisicao(self, ano: str, jogo: str):
        with httpx.Client() as client:
            response = client.get(self.url.format(ano=ano, jogo=jogo))
            with NamedTemporaryFile(delete=False, suffix=".pdf") as file:
                file.write(response.content)
                return file.name


class Crawler:
    def __init__(self):
        self.PDF_downloader = PDFDownloader()
        self.erros = []

    def pegar_todos_jogos(self):
        anos = ["2022", "2023"]
        jogos = range(1, 375 + 1)
        for ano in anos:
            for jogo in jogos:
                try:
                    print(f"Ano: {ano} - Jogo: {jogo}")
                    pdf = self.PDF_downloader.requisicao(ano, jogo)

                    yield PDFHandler(pdf).sumula()
                except Exception as e:
                    breakpoint()

