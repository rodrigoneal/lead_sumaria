# Extração de Súmulas em PDF – Série A e Copa do Brasil

Projeto desenvolvido por **Rodrigo O'Neal**.

Este projeto realiza a **extração automática dos dados presentes nas súmulas oficiais** dos campeonatos **Brasileirão Série A** e **Copa do Brasil**, diretamente de arquivos PDF.

A aplicação organiza e interpreta as informações brutas da súmula, transformando tudo em um **JSON limpo, estruturado e fácil de consumir**.

---

## ✨ Principais Recursos
- Extração de texto das súmulas em PDF.
- Limpeza e padronização das informações.
- Conversão dos dados para **JSON estruturado**.
- Foco nos padrões das súmulas da **Série A** e **Copa do Brasil**.
- Código simples, direto e fácil de integrar em outros sistemas.

---

## 🚀 Como Usar
Esta é uma **API FastAPI**, portanto você **não precisa enviar o PDF**.  
Basta informar:

- **Ano da partida** (ex: `2023`)
- **Número do jogo** (ex: `10`)
- **Tipo de competição** (`campeonato brasileiro` ou `copa do brasil`)

A API faz o **download automático** da súmula diretamente do site da CBF e retorna os dados já convertidos para JSON.

**Exemplo de requisição:**
```
GET /sumula/2023/10?competicao=copa%20do%20brasil
```


---

## ✅ Exemplo de Saída
```json
{
  "jogo": "Flamengo x Palmeiras",
  "data": "2024-06-12",
  "estadio": "Maracanã",
  "arbitro": "Fulano da Silva",
  "eventos": [
    {"tipo": "gol", "jogador": "Pedro", "minuto": 27},
    {"tipo": "cartao", "jogador": "Gerson", "cor": "amarelo"}
  ]
}
```

---

## 🧑‍💻 Autor
**Rodrigo O'Neal**

Se quiser adicionar novos padrões de súmulas ou integrar a outro projeto, é só falar comigo. 💬
