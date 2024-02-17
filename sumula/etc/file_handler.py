import tempfile
from pathlib import Path


def deletar_temp():
    path = Path(tempfile.gettempdir())
    for file in path.glob("*.pdf"):
        print(f"Deletando >>>> {file.name}")
        file.unlink(missing_ok=True)
