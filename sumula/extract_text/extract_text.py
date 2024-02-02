import re
import tabula


def extrair_dados_partida(texto: str):
    re.compile(r"ON-LINE([\s\S]*?)Arbitragem")
    texto = re.search(r"ON-LINE([\s\S]*?)Arbitragem", texto).group(1)
    return texto


def limpar_dados_partida(texto: str):
    breakpoint()
    regex = re.compile(
        r"Data: (\d{2}/\d{2}/\d{4}) Horário: (\d{2}:\d{2}) Estádio: (.+)"
    )
    return regex.search(texto).group(1, 2, 3)


def extrair_dados_partida_e_limpar(texto: str):
    dados_partida = limpar_dados_partida(extrair_dados_partida(texto))
    return {
        "data": dados_partida[0],
        "horario": dados_partida[1],
        "estadio": dados_partida[2],
    }


def extrair_dados_arbitragem(texto: str):
    texto = re.search(r"Arbitragem([\s\S]*?)Cronologia", texto).group(1)
    return texto


def limpar_dados_arbitragem(texto: str):
    arbitros = []
    dados = texto.splitlines()
    for dado in dados:
        if dado:
            try:
                cargo, nome = dado.split(":")
                arbitros.append({"Cargo": cargo.strip(), "Nome": nome.strip()})
            except ValueError:
                pass
    return arbitros


def extrair_dados_cronologia(texto: str):
    regex = re.compile(r"Cronologia([\s\S]*?)Relação")
    return regex.search(texto).group(1)


def limpar_dados_cronologia(texto: str):
    cronologia = []
    listas_textos = texto.splitlines()[2:]
    for lista_texto in listas_textos:
        dados = lista_texto.strip().split("     ")
        try:
            coluna_direita = dados[0].split(":", 1)
            coluna_esquerda = dados[1].split(":", 1)
            temp = {
                coluna_direita[0].strip(): coluna_direita[1].strip(),
                coluna_esquerda[0].strip(): coluna_esquerda[1].strip(),
            }
            cronologia.append(temp)
        except IndexError:
            pass
    return cronologia


def extrair_relacao_jogadores(pdf):
    tables = tabula.read_pdf_with_template(pdf, "template_jogadores.json")
    df = tables[-1]
    colunas = df.iloc[1, 0:6]
    nome_time_casa = df.iloc[0, 0]
    nome_time_visitante = df.iloc[0, 2]
    escalacao_casa = df.iloc[2:-1, 0:6]
    escalacao_casa.columns = colunas
    escalacao_casa.dropna(inplace=True, how="all")
    mandante = {
        "time": nome_time_casa,
        "escalacao": escalacao_casa.to_dict(orient="records"),
    }
    escalacao_visitante = df.iloc[2:-1, 6:]
    escalacao_visitante.columns = colunas
    escalacao_visitante.dropna(inplace=True, how="all")
    visitante = {
        "time": nome_time_visitante,
        "escalacao": escalacao_visitante.to_dict(orient="records"),
    }
    return [mandante, visitante]


def extrair_comissao_tecnica(text: str):
    regex = re.compile(r'Técnica([\s\S]*?)Gols')
    correspondencia = regex.search(text)
    return correspondencia.group(1).splitlines()[2:]

def limpar_comissao_tecnica(comissao: list[str], nome_mandante: str, nome_visitante: str):
    mandante = []
    visitante = []
    equipe_atual = mandante

    for item in comissao:
        if nome_visitante in item:
            item = item.replace(nome_visitante, "")
            equipe_atual.append(item)
            equipe_atual = visitante
            continue
        equipe_atual.append(item)
    return {
        nome_mandante: mandante,
        nome_visitante: visitante
    }
