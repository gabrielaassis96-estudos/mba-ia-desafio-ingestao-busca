import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

COLLECTION_NAME = "documentos"


def search(query: str, k: int = 10):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    return results