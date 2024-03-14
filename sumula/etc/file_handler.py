import tempfile
from pathlib import Path

from sumula.logger import logger


def deletar_temp():
    path = Path(tempfile.gettempdir())
    for file in path.glob("*.pdf"):
        logger.info(f"Deletando arquivo temporário: {file}")
        file.unlink(missing_ok=True)

class async_iterator_wrapper:
    def __init__(self, obj):
        self._it = iter(obj)
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value