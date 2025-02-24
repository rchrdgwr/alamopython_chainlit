
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant

# 2 functions to support RAG:
# 1. load_file - loads the pdf file and splits it into chunks
# 2. process_embeddings - creates a vector store and adds the chunks to it


def load_file(file, chunk_size=1000, chunk_overlap=200):
    loader = PyMuPDFLoader(file.path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(documents)

    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{i}"
    return docs


def process_embeddings(docs):
    embeddings = OpenAIEmbeddings()
    client = QdrantClient(":memory:")

    client.recreate_collection(
        collection_name="my_documents",
        vectors_config={
            "size": 1536,  # OpenAI embeddings dimension
            "distance": "Cosine"
        }
    )

    vectorstore = Qdrant(
        client=client,
        collection_name="my_documents",
        embeddings=embeddings
    )
    vectorstore.add_documents(docs)
    return vectorstore.as_retriever()
