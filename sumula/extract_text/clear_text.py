def remover_texto(texto: str):
    remover = ("AT - Assistente Técnico", "TC - Técnico", "Motivo: ", "PF - Preparador Físico") * 2
    for texto_remover in remover:
        texto = texto.replace(texto_remover, "")
    return texto