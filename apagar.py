from sumula.extract_text.pdf_handler import Crawler
from tinydb import TinyDB


db = TinyDB('db.json')

crawler = Crawler()
for i in crawler.pegar_todos_jogos():
    db.insert(i.model_dump())
breakpoint()