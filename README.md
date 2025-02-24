# alamopython_chainlit

Chainlit tutorial for Alamo Python February 2025 session

Key apps:

* app_1.py - basic Chainlit app to demonstrate the framework
* app_2.py - simple chatbot using OpenAI
* app_3.py - simple chatbot with manual conversational memor
* app_4.py - simple chatbot with chainlit conversational memory
* app_5.py - simple chatbot using langchain
* app_6.py - simple chatbot using langchain with streaming response
* app_7.py - chatbot with naive RAG
* app_8.py - chatbot with RAG and vector database
* app_9.py - simple chatbot with additional Chainlit features

To run: chainlit run app_n.py

# To Install on Windows:

git clone git@github.com:your-username/your-repo.git

cd your-repo

## Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt

# To install on macOS/Linux

git clone git@github.com:your-username/your-repo.git

cd your-repo

## Create and activate a virtual environment

python -m venv venv
source venv/bin/activate

## Install dependencies

pip install -r requirements.txt

## Setup Environment Variables

Copy the `.env.example` file and rename it to `.env`:

Windows:

```bash
copy .env.example .env
```

macOS/Linux

```bash
cp .env.example .env
```

Update .env with your OpenAI API key

## Helpful Links

Chainlit - https://github.com/Chainlit/chainlit

Chainlit documentation - https://docs.chainlit.io/get-started/overview

Qdrant documentation - https://qdrant.tech/documentation/

LangChain - https://www.langchain.com/
