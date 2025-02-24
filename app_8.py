import chainlit as cl
import os

from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from langchain_openai import ChatOpenAI
from utilities import load_file, process_embeddings

"""
 app_8: Chatbot with RAG and vector store
 to run: chainlit run app_8.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

user_template = """
        Question:
        {question}
   
        Context:
        {context}
    """

system_template = """
    You are a helpful assistant who always speaks in a pleasant tone!
    You are asked a question.
    You will be provided context that you must use to answer the question.
    Answer the question based only on the context.
    If you cant answer the question based on the content, say "It is not mentioned in the context"
"""


# On Chat Start - used for pre-session setup #
@cl.on_chat_start
async def start():
    # define the prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
        ("system", "Context: {context}")
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
    msg = "Hello! I'm the Alamo Python AI document chatbot with RAG"
    await cl.Message(content=msg).send()
    msg = "Upload a .pdf document and I'll answer any questions you have about it!"
    await cl.Message(content=msg).send()

    files = None
    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a .pdf file to begin processing!",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    pdf_file = files[0]
    # process the pdf file - load the file and split it into chunks
    docs = load_file(pdf_file)
    # process the embeddings - create a vector store and add the chunks to it
    retriever = process_embeddings(docs)
    # set the retriever in the user session
    cl.user_session.set("retriever", retriever)
    print(f"Number of chunks: {len(docs)}")
    await cl.Message(
        content=f"Number of chunks: {len(docs)}"
    ).send()

    await cl.Message(
        content=f"You can now ask questions about `{pdf_file.name}`."
    ).send()


# On Message - used for processing each user message #
@cl.on_message
async def on_message(message):
    try:
        # get the chain from the user session
        chain = cl.user_session.get("chain")
        chat_history = cl.user_session.get("chat_history", [])
        # get the question from the user message
        question = message.content
        # get the retriever from the user session
        retriever = cl.user_session.get("retriever")
        # get the relevant documents from the retriever
        relevant_docs = await retriever.ainvoke(question)
        print(f"Number of relevant documents found: {len(relevant_docs)}")
        for doc in relevant_docs:
            print(f"Document: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            print("-"*100)
        # combine document chunks
        context = "\n\n".join(doc.page_content for doc in relevant_docs)
        # combine document and question

        # Add user message to history
        chat_history.append(HumanMessage(content=question))
        # Create an empty message object for streaming
        msg = cl.Message(content="")
        # init variable to store response chunks
        full_response = ""
        # Invoke the chain asynchronously with streaming
        async for chunk in chain.astream(
            {"question": question,
                "context": context,
                "chat_history": chat_history},
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            if chunk.content:  # Ensure the chunk contains content
                await msg.stream_token(chunk.content)
                full_response += chunk.content

        # Send the final streamed message
        await msg.send()

        # Add AI response to history
        chat_history.append(AIMessage(content=full_response))
    except Exception as e:
        await cl.Message(
            content=f"Error processing your request: {str(e)}"
        ).send()
