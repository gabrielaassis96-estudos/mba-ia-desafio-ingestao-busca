import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from search import search


load_dotenv()


PROMPT = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def main():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    while True:
        pergunta = input("\nPERGUNTA: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            break

        resultados = search(pergunta, k=10)

        contexto = "\n\n".join(
            document.page_content
            for document, score in resultados
        )

        prompt = PROMPT.format(
            contexto=contexto,
            pergunta=pergunta,
        )

        resposta = llm.invoke(prompt)

        print("\nRESPOSTA:")
        print(resposta.content)


if __name__ == "__main__":
    main()