import tempfile
from pathlib import Path

from sumula.log import logger


def deletar_temp():
    path = Path(tempfile.gettempdir())
    for file in path.glob("*.pdf"):
        logger.info(f"Deletando arquivo temporário: {file}")
        file.unlink(missing_ok=True)
