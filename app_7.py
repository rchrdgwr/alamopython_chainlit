import chainlit as cl
import os

from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from langchain_openai import ChatOpenAI

from PyPDF2 import PdfReader

"""
 app_7: Simple AI Chatbot with naive RAG

 to run: chainlit run app_7.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

user_template = """
        Question:
        {question}

    """

system_template = """
    You are a helpful assistant who always speaks in a pleasant tone!
    You are given a document and a question.
    Answer the question based on the document.
    If you cant answer the question based on the document, say "It is not mentioned in the document"
"""


# On Chat Start - used for pre-session setup #
@cl.on_chat_start
async def start():
    # define the prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    # define the model
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    # define the chat history
    cl.user_session.set("chat_history", [])

    # define the chain
    simple_chain = chat_prompt | chat_model

    # set the chain in the user session
    cl.user_session.set("chain", simple_chain)

    # send a message to the user
    msg = "Hello! I'm the Alamo Python AI document chatbot"
    await cl.Message(content=msg).send()
    msg = "Upload a .pdf document and I'll answer any questions you have about it!"
    await cl.Message(content=msg).send()

    files = None
    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a .pdf file to begin processing!",
            accept=["application/pdf"],
            max_size_mb=10,
            timeout=180,
        ).send()

    pdf_file = files[0]
    # read the pdf file
    pdf_reader = PdfReader(pdf_file.path)
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text()

    # Extract text from all pages
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text()

    # # Store full document in session
    cl.user_session.set("full_document", full_text)

    await cl.Message(
        content=f"`{pdf_file.name}` uploaded, it contains {len(full_text)} chars"
    ).send()

    await cl.Message(
        content=f"You can now ask questions about `{pdf_file.name}`."
    ).send()


# On Message - used for processing each user message #
@cl.on_message
async def on_message(message):
    # get the chain from the user session
    chain = cl.user_session.get("chain")
    chat_history = cl.user_session.get("chat_history", [])
    full_document = cl.user_session.get("full_document", "")
    # get the question from the user message
    question = message.content
    # combine document and question
    context_with_doc = f"Document:\n{full_document}\n\nUser Question: {question}"
    # Add user message to history
    chat_history.append(HumanMessage(content=context_with_doc))
    # Create an empty message object for streaming
    msg = cl.Message(content="")
    # init variable to store response chunks
    full_response = ""
    # Invoke the chain asynchronously with streaming
    async for chunk in chain.astream(
        {"chat_history": chat_history},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        if chunk.content:  # Ensure the chunk contains content
            await msg.stream_token(chunk.content)
            full_response += chunk.content

    # Send the final streamed message
    await msg.send()

    # Add AI response to history
    chat_history.append(AIMessage(content=full_response))
