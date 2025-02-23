import chainlit as cl
import os

from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

"""
 app_5: Simple AI Chatbot with LangChain and OpenAI

 to run: chainlit run app_5.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

user_template = """
        Question:
        {question}

    """

system_template = """
    You are a helpful assistant who always speaks in a pleasant tone!
    Do your best to answer the question succinctly and truthfully.
    Think through your answers carefully.
    Respond in the language provided below.
    If no language is provided, use English.
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
    msg = "Hello! I'm the Alamo Python AI chatbot. Ask me a question!"
    await cl.Message(content=msg).send()


# On Message - used for processing each user message #
@cl.on_message
async def on_message(message):
    # get the chain from the user session
    chain = cl.user_session.get("chain")
    chat_history = cl.user_session.get("chat_history", [])
    # get the question from the user message
    question = message.content
    # Add user message to history
    chat_history.append(HumanMessage(content=question))
    # invoke the chain
    response = chain.invoke({"chat_history": chat_history})
    # Extract AI response
    ai_response = response.content
    # Add AI response to history
    chat_history.append(AIMessage(content=ai_response))
    # print the response
    print(response.content)
    # send the response to the user
    await cl.Message(content=ai_response).send()
