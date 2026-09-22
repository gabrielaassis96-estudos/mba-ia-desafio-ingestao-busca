Ingestão e Busca Semântica com LangChain e PostgreSQL

Projeto desenvolvido como solução para o desafio de Ingestão e Busca Semântica com LangChain e PostgreSQL + pgVector.

A aplicação permite:

Ler um arquivo PDF;
Dividir o conteúdo em chunks;
Gerar embeddings para cada chunk;
Armazenar os embeddings no PostgreSQL utilizando pgVector;
Realizar busca semântica a partir de perguntas feitas via terminal;
Utilizar uma LLM para gerar respostas baseadas exclusivamente no conteúdo recuperado do PDF;
Informar quando não existem informações suficientes no contexto para responder.
Arquitetura

O projeto utiliza uma arquitetura simples de RAG (Retrieval-Augmented Generation):

                    INGESTÃO

                 document.pdf
                      │
                      ▼
                PyPDFLoader
                      │
                      ▼
          RecursiveCharacterTextSplitter
             chunk_size = 1000
             overlap = 150
                      │
                      ▼
                  Embeddings
                      │
                      ▼
              PostgreSQL + pgVector
                      │
                      │
                      ▼
                    BUSCA

             Pergunta do usuário
                      │
                      ▼
                  Embedding
                      │
                      ▼
           Busca semântica (k=10)
                      │
                      ▼
                  Contexto
                      │
                      ▼
                     LLM
                      │
                      ▼
                   Resposta
Tecnologias utilizadas
Python
LangChain
PostgreSQL
pgVector
Docker
Docker Compose
OpenAI Embeddings
OpenAI LLM
PyPDF
Estrutura do projeto
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── document.pdf
├── README.md
└── src/
    ├── ingest.py
    ├── search.py
    └── chat.py
src/ingest.py

Responsável por:

Carregar o PDF;
Dividir o conteúdo em chunks de 1000 caracteres;
Utilizar overlap de 150 caracteres;
Gerar embeddings;
Armazenar os documentos e embeddings no PostgreSQL com pgVector.
src/search.py

Responsável pela busca semântica.

A pergunta do usuário é transformada em embedding e utilizada para encontrar os 10 chunks mais relevantes no banco de dados.

src/chat.py

Responsável pela interação via terminal.

O script:

Recebe a pergunta;
Executa a busca semântica;
Recupera os 10 resultados mais relevantes;
Monta o contexto;
Envia o contexto e a pergunta para a LLM;
Exibe a resposta no terminal.
Requisitos

Antes de executar o projeto, instale:

Python 3
Docker Desktop
Docker Compose
Uma API Key da OpenAI

No Windows, recomenda-se utilizar o Docker Desktop com WSL 2.

Configuração
1. Clone o projeto
git clone https://github.com/SEU-USUARIO/mba-ia-desafio-ingestao-busca.git

Entre na pasta:

cd mba-ia-desafio-ingestao-busca
2. Crie o ambiente virtual
Windows

No PowerShell:

python -m venv venv

Ative:

.\venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
pip install -r requirements.txt
4. Configure as variáveis de ambiente

Copie o arquivo .env.example:

Windows PowerShell
Copy-Item .env.example .env
Linux / macOS
cp .env.example .env

Edite o .env:

OPENAI_API_KEY=sua_api_key

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag

Nunca envie o arquivo .env para o GitHub. Ele contém informações sensíveis.

Banco de dados

O projeto utiliza PostgreSQL com pgVector através do Docker.

O docker-compose.yml configura:

PostgreSQL 17;
extensão pgVector;
banco de dados rag;
usuário postgres;
senha postgres;
porta 5432.

Para iniciar o banco:

docker compose up -d

Verifique os containers:

docker compose ps

O PostgreSQL deve estar em execução.

Para verificar os logs:

docker compose logs
Ingestão do PDF

Coloque o arquivo PDF utilizado pelo projeto na raiz com o nome:

document.pdf

A estrutura deve ficar:

├── document.pdf
├── docker-compose.yml
├── requirements.txt
└── src/

Com o banco em execução, execute:

python src/ingest.py

O processo realiza:

PDF
 ↓
PyPDFLoader
 ↓
Chunks de 1000 caracteres
 ↓
Overlap de 150 caracteres
 ↓
Embeddings
 ↓
PostgreSQL + pgVector

Ao final, os chunks e seus embeddings estarão armazenados no banco de dados.

Busca semântica

A busca utiliza:

similarity_search_with_score(query, k=10)

Isso significa que, para cada pergunta, são recuperados os 10 resultados mais relevantes semanticamente.

Por exemplo:

PERGUNTA:
Qual foi o faturamento da empresa?

Mesmo que o PDF utilize uma frase diferente, como:

O faturamento registrado pela empresa foi de 10 milhões de reais.

a busca semântica pode recuperar esse trecho por similaridade de significado.

Chat via CLI

Depois de realizar a ingestão:

python src/chat.py

A aplicação ficará aguardando perguntas:

PERGUNTA:

Exemplo:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA: O faturamento foi de 10 milhões de reais.
Perguntas fora do contexto

A aplicação deve responder:

Não tenho informações necessárias para responder sua pergunta.

quando a informação solicitada não estiver disponível no contexto recuperado do PDF.

Exemplo:

PERGUNTA: Qual é a capital da França?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

Outro exemplo:

PERGUNTA: Quantos clientes temos em 2024?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
Regras utilizadas pela LLM

A LLM recebe o contexto recuperado do banco e deve seguir as seguintes regras:

CONTEXTO:
{resultados encontrados no banco}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

Dessa forma, a resposta é fundamentada no conteúdo recuperado do documento.

Fluxo completo de execução

A execução completa do projeto é:

1. Iniciar o PostgreSQL
docker compose up -d
2. Ativar o ambiente virtual

Windows:

.\venv\Scripts\Activate.ps1

Linux/macOS:

source venv/bin/activate
3. Realizar a ingestão
python src/ingest.py
4. Iniciar o chat
python src/chat.py
Testes

Foram considerados os seguintes cenários:

Pergunta respondível
PERGUNTA: Qual o faturamento da empresa?

A resposta deve utilizar informações presentes no PDF.

Pergunta semanticamente equivalente

Uma pergunta pode utilizar palavras diferentes das utilizadas no documento.

Exemplo:

PERGUNTA: Quanto dinheiro a empresa faturou?

A busca deve utilizar similaridade semântica para encontrar os trechos relevantes.

Pergunta fora do contexto
PERGUNTA: Qual é a capital da França?

Resposta esperada:

Não tenho informações necessárias para responder sua pergunta.
Pergunta que solicita opinião
PERGUNTA: Você acha que a empresa é boa?

Resposta esperada:

Não tenho informações necessárias para responder sua pergunta.
Observações
Embeddings

O projeto utiliza um modelo de embeddings para transformar os chunks do documento e as perguntas do usuário em vetores.

O modelo de embeddings deve ser o mesmo durante a ingestão e durante as consultas.

A dimensão dos vetores depende do modelo escolhido.

Por esse motivo, caso o modelo de embeddings seja alterado após a criação da collection, pode ser necessário remover os dados vetoriais existentes e executar a ingestão novamente.

PostgreSQL + pgVector

O PostgreSQL é utilizado como banco de dados vetorial através da extensão pgVector.

O banco é executado através do Docker Compose, permitindo reproduzir o ambiente de desenvolvimento sem necessidade de instalar o PostgreSQL diretamente na máquina.

Comandos úteis

Ver containers:

docker compose ps

Ver logs:

docker compose logs

Parar os containers:

docker compose down

Parar os containers e remover os volumes:

docker compose down -v

O comando docker compose down -v remove o volume do PostgreSQL e, consequentemente, os dados armazenados no banco. Utilize-o apenas quando quiser reiniciar a base de dados do zero.

Licença

Projeto desenvolvido para fins educacionais como parte do desafio de implementação de ingestão e busca semântica com LangChain, PostgreSQL e pgVector.