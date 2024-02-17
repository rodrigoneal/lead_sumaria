import re
import tabula

from sumula.extract_text.clear_text import remover_texto


def dados_jogo_numero(texto: str):
    return re.search(r"Jogo:([\s\S]*?)CBF - ", texto).group(1).strip()


def extrair_dados_partida(texto: str):
    return re.search(r"ON-LINE([\s\S]*?)Arbitragem", texto).group(1)


def limpar_dados_partida(texto: str):
    campeonato = re.search(r"Campeonato:([\s\S]*?)Rodada:", texto).group(1).strip()
    rodada = re.search(r"Rodada:([\s\S]*?)Jogo:", texto).group(1).strip()
    jogo = re.search(r"Jogo:([\s\S]*?)Data:", texto).group(1).strip()
    data = re.search(r"Data:([\s\S]*?)Horário:", texto).group(1).strip()
    horario = re.search(r"Horário:([\s\S]*?)Estádio:", texto).group(1).strip()
    estadio = re.search(r"Estádio:([\s\S]*)", texto).group(1).strip()
    mandante, visitante = jogo.split(" X ")
    ano = data.split("/")[-1]
    return {
        "campeonato": campeonato,
        "rodada": rodada,
        "jogo": jogo,
        "data": data,
        "horario": horario,
        "estadio": estadio,
        "mandante": mandante,
        "visitante": visitante,
        "ano": ano,
    }


def dados_partida(texto: str) -> dict[str, str]:
    dados = extrair_dados_partida(texto)
    return limpar_dados_partida(dados)


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
                arbitros.append({"funcao": cargo.strip(), "nome": nome.strip()})
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
        if len(dados) == 1:
            if "Atraso" in dados[0]:
                key_name = "Atraso"
                dados = dados[0].split("Atraso")
            elif "Acréscimo" in dados[0]:
                key_name = "Acréscimo"
                dados = dados[0].split("Acréscimo")
            elif "Resultado" in dados[0]:
                key_name = "Resultado"
                dados = dados[0].rsplit("Resultado", 1)
            else:
                breakpoint()

            _temp = f"{key_name} {dados[-1].strip()}"
            dados[-1] = _temp

        try:
            coluna_direita = dados[0].split(":", 1)
            coluna_esquerda = dados[1].split(":", 1)
            temp = {
                coluna_direita[0]
                .strip(): coluna_direita[1]
                .strip()
                .replace("2º Tempo", ""),
                coluna_esquerda[0]
                .strip(): coluna_esquerda[1]
                .strip()
                .replace("2º Tempo", ""),
            }
            cronologia.append(temp)
        except IndexError:
            pass
    if "Penalti" in dados[-1]:
        penalti = dados[-1].split(":")
        cronologia.append({penalti[0].strip(): penalti[1].strip()})
    return cronologia


# [{'Entrada do mandante': '18:50', 'Atraso': 'Não Houve'}, {'Entrada do visitante': '18:50', 'Atraso': 'Não Houve'}, {'Início 1º Tempo': '19:00', 'Atraso': 'Não Houve'}, {'Término do 1º Tempo': '19:48', 'Acréscimo': '3 min'}, {'Entrada do mandante': '20:01', 'Atraso': 'Não Houve'}, {'Entrada do visitante': '20:01', 'Atraso': 'Não Houve'}, {'Início do 2º Tempo': '20:03', 'Atraso': 'Não Houve'}, {'Término do 2º Tempo': '20:56', 'Acréscimo': '8 min'}, {'Resultado do 1º Tempo': '1 X 2', 'Resultado Final': '3 X 2'}]

def dados_cronologogia(texto: str) -> list[dict[str, str]]:
    dados = extrair_dados_cronologia(texto)
    return limpar_dados_cronologia(dados)


def extrair_relacao_jogadores(pdf, template):
    tables = tabula.read_pdf_with_template(pdf, template)
    df = tables[-1]
    try:
        if df.iloc[-1, 0].startswith("T = "):
            df = df.iloc[:-1, :]
    except AttributeError:
        pass
    colunas = df.iloc[1, 0:6]
    try:
        nome_time_casa, nome_time_visitante = df.iloc[0, :].dropna()
    except ValueError:
        return
    escalacao_casa = df.iloc[2:, 0:6].dropna(how="all")
    escalacao_casa.columns = colunas
    mandante = {
        "time": nome_time_casa,
        "escalacao": escalacao_casa.fillna("").to_dict(orient="records"),
    }
    escalacao_visitante = df.iloc[2:, 6:].dropna(how="all")
    escalacao_visitante.columns = colunas
    visitante = {
        "time": nome_time_visitante,
        "escalacao": escalacao_visitante.fillna("").to_dict(orient="records"),
    }
    return [mandante, visitante]


# Segunda Pagina


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
            equipe_atual.append({"cargo": cargo.strip(), "nome": nome.strip()})
            equipe_atual = visitante
            continue
        equipe_atual.append({"cargo": cargo.strip(), "nome": nome.strip()})
    return {nome_mandante: mandante, nome_visitante: visitante}


def dados_comissao_tecnica(texto: str, nome_mandante: str, nome_visitante: str):
    dados = extrair_comissao_tecnica(texto)
    return limpar_comissao_tecnica(dados, nome_mandante, nome_visitante)


def extrair_dados_gols(text: str):
    regex = re.compile(r"Gols([\s\S]*?)NR = Normal")
    correspondencia = regex.search(text)
    if correspondencia:
        return correspondencia.group(1).splitlines()[2:]
    return []


def limpar_dados_gols(dados_gols: list[str], mandante: str, visitante: str):
    gols = []
    _mandante = mandante.replace(" / ", "/")
    _visitante = visitante.replace(" / ", "/")
    for dado in dados_gols:
        hora_gol = re.search(r"(\+(\d+)|\d+:\d+)", dado).group()
        tempo_jogo = re.search(r"(\d+[Tt])", dado).group()
        numero_jogador = re.search(r"T(\d+)", dado).group(1)
        tipo_de_gol = re.search(r"(NR|PN|CT|FT)", dado).group(1)
        dados = re.search(r"(NR|PN|CT|FT)(.*)", dado).group(2)
        if _mandante in dados:
            time_jogador = _mandante
        elif _visitante in dados:
            time_jogador = _visitante
        nome_jogador = dados.replace(time_jogador, "")
        gols.append(
            {
                "hora_gol": hora_gol.strip(),
                "tempo_jogo": tempo_jogo.strip(),
                "numero_jogador": numero_jogador.strip(),
                "tipo_gol": tipo_de_gol.strip(),
                "nome_jogador": nome_jogador.strip(),
                "time": time_jogador.strip(),
            }
        )
    return gols


def dados_gols(texto: str, mandante: str, visitante: str):
    dados = extrair_dados_gols(texto)
    return limpar_dados_gols(dados, mandante, visitante)


def extrair_dados_cartao_amarelos(text: str):
    regex = re.compile(r"Cartões Amarelos([\s\S]*?)Cartões Vermelhos")
    correspondencia = regex.search(text)
    if correspondencia:
        return correspondencia.group(1)
    breakpoint()


def limpar_dados_cartao_amarelos(dados_cartao: str, mandante: str, visitante: str):
    padroes = re.split(r"(?<=\n|\s)(?=\d{2}:\d{2}|\+\d{2}:\d{2})", dados_cartao)
    amarelos = []

    # sub = re.compile(
    #     r"(\+?\d+:\d+)\s*([12]T)\s*(\d+[A-Z]\d+)?(\d+\w+ [\w\s\/]+) Motivo: ([\w\.\s\-]+)"
    # )
    def numero_or_tecnico(text: str):
        numero = re.search(r"\d+", text)
        if numero:
            return numero.group()
        return text

    _mandante = mandante.rsplit("/")[0].strip()
    _visitante = visitante.rsplit("/")[0].strip()
    padroes = padroes[1:]
    for padrao in padroes:
        dados, *motivo = padrao.splitlines()
        horario, dados = dados.split(" ", 1)
        tempo = dados[:2]
        if _mandante in dados:
            equipe = mandante
        elif _visitante in dados:
            equipe = visitante
        else:
            breakpoint()
        _equipe = equipe.replace(" / ", "/")
        dados = dados.replace(_equipe, "").strip()
        dados = dados.replace(tempo, "").strip()
        numero = numero_or_tecnico(dados[0:2])
        nome = dados.replace(numero, "").strip()
        motivo = " ".join(motivo)
        amarelos.append(
            {
                "hora_cartao": horario,
                "tempo_jogo": tempo,
                "numero_jogador": numero,
                "nome_jogador": nome,
                "time": equipe,
                "motivo": remover_texto(motivo),
            }
        )
    return amarelos


def dados_cartao_amarelo(texto: str, mandante: str, visitante: str):
    dados = extrair_dados_cartao_amarelos(texto)
    return limpar_dados_cartao_amarelos(dados, mandante, visitante)


def extrair_dados_cartao_vermelhos(text: str):
    regex = re.compile(r"Cartões Vermelhos([\s\S]*?)Confederação Brasileira")
    correspondencia = regex.search(text)
    if correspondencia:
        return correspondencia.group(1).replace("\nTempo 1T/2TNºNome do Jogador\n", "")
    breakpoint()


def limpar_dados_cartao_vermelho(text: str):
    try:
        if "\nNÃO HOUVE EXPULSÕES\n" in text:
            return []
    except TypeError:
        breakpoint()
    padrao = r"\d+:\d+|\+\d+:\d+|-PJ"
    padrao_horario = r"(\d+:\d+|\+\d+:\d+|-PJ)"
    textos = re.split(padrao, text)
    if not textos[0] or "NºNome do Jogador" in textos[0]:
        textos = textos[1:]
    horarios = re.findall(padrao_horario, text)
    dados_cartoes = []
    for contador, texto in enumerate(textos):
        try:
            cartao = re.search(r"\n(.*?)(?:Motivo:|$)", texto).group(1)
        except AttributeError:
            continue
        try:
            hora = horarios[contador] if not horarios[contador].startswith("-") else "-"
        except IndexError:
            breakpoint()
        try:
            tempo = re.search(r"\s([12][Tt])", texto).group(1)
        except AttributeError:
            if hora == "-":
                tempo = horarios[contador][1:]
            else:
                tempo = texto.strip()[:3]
        try:
            numero_jogador = re.search(r"T(\d{1,3})[^-]+-([^-]+)", texto).group(1)
        except AttributeError:
            numero_jogador = texto.strip().replace(tempo, "")[:2]
        try:
            nome_jogador = (
                re.search(r"T(\d{1,3})[^-]+-([^-]+)", texto)
                .group(0)
                .split("-")[0]
                .replace(f"T{numero_jogador}", "")
                .strip()
            )
        except AttributeError:
            nome_jogador = (
                texto.strip()
                .replace(tempo + numero_jogador, "")
                .strip()
                .split("-")[0]
                .strip()
            )
        motivo = texto.split("Motivo:")[-1].replace("\n", " ").strip()
        time = texto.split("\n", 1)[0].split("-")[-1].strip()

        dados_cartoes.append(
            {
                "aplicado": cartao,
                "hora_cartao": hora,
                "tempo_jogo": tempo,
                "numero_jogador": numero_jogador,
                "nome_jogador": nome_jogador,
                "time": time,
                "motivo": remover_texto(motivo),
            }
        )
    return dados_cartoes


def dados_cartao_vermelho(texto: str):
    dados = extrair_dados_cartao_vermelhos(texto)
    return limpar_dados_cartao_vermelho(dados)


def extrair_dados_ocorrencias(texto: str):

    regex = re.compile(
        r"Ocorrências / Observações([\s\S]*?)Motivo de atraso no início e/ou"
    )
    return regex.search(texto).group(1)


def limpar_dados_ocorrencias(texto: str):
    return texto.replace("\n", " ").strip()


def dados_ocorrencias(texto: str):
    dados = extrair_dados_ocorrencias(texto)
    return limpar_dados_ocorrencias(dados)


def extrair_dados_acrescimos(texto: str):
    regex = re.compile(
        r"e/ou reinício, e de acréscimos:([\s\S]*?)Observações Eventuais"
    )
    return regex.search(texto).group(1)


def limpar_dados_acrescimos(texto: str):
    return texto.replace("\n", " ").strip()


def dados_acrescimos(texto: str):
    dados = extrair_dados_acrescimos(texto)
    return limpar_dados_acrescimos(dados)


def extrair_dados_observacoes_eventuais(texto: str):
    try:
        return re.search(
            r"Observações Eventuais([\s\S]*?)Relatório do Assistente", texto
        ).group(1)
    except AttributeError:
        return re.search(r"Observações Eventuais([\s\S]*?)Substituições", texto).group(
            1
        )


def limpar_dados_observacoes_eventuais(texto: str):
    return texto.replace("\n", " ").strip()


def dados_observacoes_eventuais(texto: str):
    dados = extrair_dados_observacoes_eventuais(texto)
    return limpar_dados_observacoes_eventuais(dados)


def extrair_dados_relatorio_assistente(texto: str):
    regex = re.compile(r"Relatório do Assistente([\s\S]*?)Substituições")
    try:
        return regex.search(texto).group(1)
    except AttributeError:
        return "Nada a relatar."


def limpar_dados_relatorio_assistente(texto: str):
    return texto.replace("\n", " ").strip()


def dados_relatorio_assistente(texto: str):
    dados = extrair_dados_relatorio_assistente(texto)
    return limpar_dados_relatorio_assistente(dados)


def dados_substituicao(pdf: str, num_page):
    tables = tabula.read_pdf(pdf, pages=num_page, stream=True)
    try:
        df = tables[-1]
    except IndexError:
        breakpoint()
    df = df.iloc[1:-1, :]
    try:
        df.columns = ["hora_substituicao", "tempo", "time", "entrou", "saiu"]
    except ValueError:
        df = df.dropna(axis=1, how="all")
        df.columns = ["hora_substituicao", "tempo", "time", "entrou", "saiu"]
    return df.to_dict("records")


def dados_substituicao_2(text: str, mandante: str, visitante: str):
    regex = re.compile(r"Substituições([\s\S]*?)Confederação Brasileira de Futebol")
    try:
        texto = regex.search(text).group(1)
    except AttributeError:
        return "Nada a relatar."
    padrao = r"\d+:\d+|\+\d+:\d+|-PJ"
    padrao_horario = r"(\d+:\d+|\+\d+:\d+|-PJ)"
    padrao_numero = r"\d+"
    horarios = re.findall(padrao_horario, texto)
    textos = re.split(padrao, texto)
    substituicoes = []
    if "Tempo 1T/2T" in textos[0]:
        textos = textos[1:]
    _mandante = mandante.replace(" / ", "/").strip()
    _visitante = visitante.replace(" / ", "/").strip()
    for contador, texto in enumerate(textos):
        texto = texto.strip()
        if _mandante in texto:
            equipe = _mandante
        elif _visitante in texto:
            equipe = _visitante
        else:
            if _mandante.rsplit(" ", 1)[0] in texto:
                equipe = _mandante
            elif _visitante.rsplit(" ", 1)[0] in texto:
                equipe = _visitante
            else:
                breakpoint()
        hora = horarios[contador]
        try:
            tempo, dados = texto.split(equipe)
        except ValueError:
            tempo, dados = texto.split(equipe.rsplit(" ",1)[0])
            dados = dados.replace("...", "").strip()
        num_entrou, dados, nome_saiu = dados.split("-")
        num_result = re.search(padrao_numero, dados)
        if num_result:
            num_saiu = num_result.group()
        else:
            num_saiu = "-"
        nome_entrou = dados.replace(num_saiu, "").strip()
        substituicoes.append(
            {
                "hora_substituicao": hora.strip(),
                "tempo": tempo.strip(),
                "time": equipe.strip(),
                "num_entrou": num_entrou.strip(),
                "entrou": nome_entrou.strip(),
                "num_saiu": num_saiu.strip(),
                "saiu": nome_saiu.strip(),
            }
        )
    return substituicoes

