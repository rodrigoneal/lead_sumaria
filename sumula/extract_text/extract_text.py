import re
import tabula


def extrair_dados_partida(texto: str):
    texto = re.search(r"ON-LINE([\s\S]*?)Arbitragem", texto).group(1)
    return texto


def limpar_dados_partida(texto: str):
    campeonato = re.search(r"Campeonato:([\s\S]*?)Rodada:", texto).group(1).strip()
    rodada = re.search(r"Rodada:([\s\S]*?)Jogo:", texto).group(1).strip()
    jogo = re.search(r"Jogo:([\s\S]*?)Data:", texto).group(1).strip()
    data = re.search(r"Data:([\s\S]*?)Horário:", texto).group(1).strip()
    horario = re.search(r"Horário:([\s\S]*?)Estádio:", texto).group(1).strip()
    estadio = re.search(r"Estádio:([\s\S]*)", texto).group(1).strip()
    return {
        "campeonato": campeonato,
        "rodada": rodada,
        "jogo": jogo,
        "data": data,
        "horario": horario,
        "estadio": estadio,
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


def dados_arbitragem(texto: str) -> list[dict[str, str]]:
    dados = extrair_dados_arbitragem(texto)
    return limpar_dados_arbitragem(dados)


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
    try:
        if df.iloc[-1, 0].startswith("T = "):
            df = df.iloc[:-1, :]
    except AttributeError:
        pass
    colunas = df.iloc[1, 0:6]
    nome_time_casa, nome_time_visitante = df.iloc[0, :].dropna()
    escalacao_casa = df.iloc[2:, 0:6].dropna(how="all")
    escalacao_casa.columns = colunas
    mandante = {
        "time": nome_time_casa,
        "escalacao": escalacao_casa.to_dict(orient="records"),
    }
    escalacao_visitante = df.iloc[2:, 6:].dropna(how="all")
    escalacao_visitante.columns = colunas
    visitante = {
        "time": nome_time_visitante,
        "escalacao": escalacao_visitante.to_dict(orient="records"),
    }
    return [mandante, visitante]


def extrair_comissao_tecnica(text: str):
    regex = re.compile(r"Técnica([\s\S]*?)Gols")
    correspondencia = regex.search(text)
    return correspondencia.group(1).splitlines()[2:]


def limpar_comissao_tecnica(
    comissao: list[str], nome_mandante: str, nome_visitante: str
):
    mandante = []
    visitante = []
    equipe_atual = mandante

    for item in comissao:
        try:
            cargo, nome = item.split(":")
        except IndexError:
            continue
        if nome_visitante in nome:
            nome = nome.replace(nome_visitante, "")
            equipe_atual.append({"Cargo": cargo.strip(), "Nome": nome.strip()})
            equipe_atual = visitante
            continue
        equipe_atual.append({"Cargo": cargo.strip(), "Nome": nome.strip()})
    return {nome_mandante: mandante, nome_visitante: visitante}


def extrair_dados_gols(text: str):
    regex = re.compile(r"Gols([\s\S]*?)NR = Normal")
    correspondencia = regex.search(text)
    return correspondencia.group(1).splitlines()[2:]


def limpar_dados_gols(dados_gols: list[str]):
    gols = []
    for dado in dados_gols:
        hora_gol = re.search(r"(\+(\d+)|\d+:\d+)", dado).group()
        tempo_jogo = re.search(r"(\d+[Tt])", dado).group()
        numero_jogador = re.search(r"T(\d+)", dado).group(1)
        tipo_de_gol = re.search(r"(NR|PN|CT|FT)", dado).group(1)
        _nome = re.search(r"(NR|PN|CT|FT)(.*)", dado).group(2)
        nome_jogador = _nome.rsplit(" ", 1)[0]
        time_jogador = _nome.rsplit(" ", 1)[1]
        gols.append(
            {
                "hora_gol": hora_gol,
                "tempo_jogo": tempo_jogo,
                "numero_jogador": numero_jogador,
                "tipo_gol": tipo_de_gol,
                "nome_jogador": nome_jogador,
                "time": time_jogador,
            }
        )
    return gols


def extrair_dados_cartao_amarelos(text: str):
    regex = re.compile(r"Cartões Amarelos([\s\S]*?)Cartões Vermelhos")
    correspondencia = regex.search(text)
    return correspondencia.group(1)


def limpar_dados_cartao_amarelos(dados_cartao: str):
    padroes = re.split(r"\n(?=\d{2}:\d{2}|\+\d{2}:\d{2})", dados_cartao)
    amarelos = []
    sub = re.compile(
        r"(\d+:\d+)\s*([12]T)\s*(\d+[A-Z]\d+)?(\d+\w+ [\w\s\/]+) Motivo: ([\w\.\s\-]+)"
    )
    for padrao in padroes:
        correspondencia = sub.search(padrao.replace("\n", " "))
        if correspondencia:
            horario = correspondencia.group(1)
            tempo = correspondencia.group(2) if correspondencia.group(2) else ""
            numero = correspondencia.group(3)
            _nome = correspondencia.group(4)
            motivo = correspondencia.group(5)
            numero = re.sub(r"[a-zA-Z]", "", _nome).split(" ")[0].strip()
            nome = re.sub(r"\d+", "", _nome).rsplit(" ", 1)[0].strip()
            equipe = _nome.rsplit(" ", 1)[1].strip()
            amarelos.append(
                {
                    "horario": horario,
                    "tempo": tempo,
                    "numero": numero,
                    "nome": nome,
                    "equipe": equipe,
                    "motivo": motivo,
                }
            )
    return amarelos
