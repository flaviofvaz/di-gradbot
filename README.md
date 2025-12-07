# GradBot

O **GradBot** é um assistente virtual baseado em RAG (Retrieval-Augmented Generation) especializado em responder perguntas com base em documentos PDF carregados pelo usuário. O projeto utiliza **Python (FastAPI)** no backend, **React** no frontend e **Qdrant** como banco de dados vetorial.

## Pré-requisitos

Antes de iniciar, você precisa ter as seguintes ferramentas instaladas:

1.  **Git**: Para clonar o repositório.
2.  **Docker Desktop**: O projeto é totalmente containerizado.
      * [Guia oficial de instalação do Docker](https://docs.docker.com/get-docker/) (Selecione seu sistema operacional: Windows, Mac ou Linux).
3.  **Chave da API da OpenAI**: O sistema requer uma chave válida (`OPENAI_API_KEY`) para gerar embeddings e respostas.

-----

## Passo a Passo para Execução

### 1\. Clonar o Repositório

Abra seu terminal e clone o projeto:

```bash
git clone https://github.com/flaviofvaz/di-gradbot.git
cd di-gradbot
```

### 2\. Configurar a Variável de Ambiente (OPENAI\_API\_KEY)

O GradBot precisa da sua chave da OpenAI para funcionar. Configure a variável `OPENAI_API_KEY` no seu terminal antes de rodar o Docker. Escolha a opção correspondente ao seu sistema operacional:

#### Linux e macOS (Bash/Zsh)

```bash
export OPENAI_API_KEY="sua-chave-aqui-sk-..."
```

#### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="sua-chave-aqui-sk-..."
```

#### Windows (CMD - Prompt de Comando)

```cmd
set OPENAI_API_KEY=sua-chave-aqui-sk-...
```

### 3\. Construir e Rodar os Containers

Com o Docker Desktop rodando e a variável configurada, execute o comando abaixo na raiz do projeto para baixar as imagens, construir o projeto e iniciar os serviços:

```bash
docker-compose up --build
```

Aguarde até que todos os serviços (`gradbot-backend`, `gradbot-frontend` e `qdrant`) estejam iniciados.

-----

## Persistência de Dados

Ao iniciar o projeto pela primeira vez, uma pasta chamada **`qdrant_data`** será criada automaticamente no diretório raiz do projeto.

  * **Propósito:** Esta pasta serve para a **persistência dos dados** do banco vetorial (Qdrant).
  * **Importante:** Ela garante que os documentos que você indexou e as coleções de vetores criadas **não sejam perdidos** quando você reiniciar ou desligar os containers Docker. Se você desejar "resetar" o banco de dados completamente, basta apagar esta pasta (com os containers parados) e iniciá-los novamente.

-----

## Acessando a Aplicação

Após a inicialização bem-sucedida, você pode acessar os componentes do sistema pelos seguintes endereços:

  * **Frontend (Chat e Gerenciamento):**

      * Acesse: [http://localhost](https://www.google.com/search?q=http://localhost)
      * *Aqui você pode fazer upload de documentos e conversar com o bot.*

  * **Backend (Documentação da API - Swagger UI):**

      * Acesse: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
      * *Útil para testar endpoints manualmente ou verificar se a API está online.*

  * **Qdrant (Banco de Dados Vetorial):**

      * Acesse: [http://localhost:6333/dashboard](https://www.google.com/search?q=http://localhost:6333/dashboard)
      * *Para visualizar as coleções de vetores criadas.*

-----

## Como Parar o Projeto

Para encerrar a execução e parar os containers, pressione `Ctrl+C` no terminal onde o projeto está rodando ou, em um novo terminal, execute:

```bash
docker-compose down
```

-----

## Solução de Problemas Comuns

  * **Erro de "API Key not set":** Certifique-se de que configurou a variável de ambiente corretamente no **mesmo terminal** onde executou o comando `docker-compose up`.
  * **Portas em uso:** Se você receber um erro informando que a porta `80` ou `8000` já está em uso, verifique se não há outros serviços (como Apache, Nginx ou outro projeto Python) rodando em sua máquina e pare-os.
  * **Frontend não conecta ao Backend:** O frontend espera que o backend esteja rodando em `http://localhost:8000`. Certifique-se de que o container do backend subiu sem erros.
