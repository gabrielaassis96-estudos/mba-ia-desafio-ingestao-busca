import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

PDF_PATH = "document.pdf"
COLLECTION_NAME = "documentos"


def main():
    print("1. Carregando PDF...")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print(f"   Páginas carregadas: {len(documents)}")

    print("2. Dividindo documento em chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"   Chunks criados: {len(chunks)}")

    print("3. Criando embeddings...")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    print("4. Salvando no PostgreSQL...")

    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    print("5. Ingestão concluída!")


if __name__ == "__main__":
    main()