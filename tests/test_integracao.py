from sumula.extract_text.pdf_handler import PDFHandler
import pytest

@pytest.mark.parametrize("num_pagina, esperado", [(0, "1/3"), (1, "2/3"), (2, "3/3")])
def test_se_pega_as_paginas(num_pagina, esperado):
    pdf_handler = PDFHandler("142317se.pdf")
    pagina = pdf_handler.pegar_pagina(num_pagina)
    assert esperado in pagina