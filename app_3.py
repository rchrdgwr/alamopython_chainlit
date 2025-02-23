import chainlit as cl
from openai import OpenAI
import os

from dotenv import load_dotenv

"""
 app_3: Simple AI Chatbot with manual conversation memory

 to run: chainlit run app_3.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

system_text = "You are a helpful and friendly chatbot."
system_message = {"role": "system", "content": system_text}

conversation_history = []


# On Chat Start - used for pre-session setup #
@cl.on_chat_start
async def start():
    global conversation_history
    conversation_history = [system_message]
    msg = "Hello! I'm the Alamo Python AI chatbot. Ask me a question!"
    await cl.Message(content=msg).send()


# On Message - used for processing each user message #
@cl.on_message
async def main(message: cl.Message):
    global conversation_history
    conversation_history.append({"role": "user", "content": message.content})

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    msg_response = chat_completion.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": msg_response})

    # Send response to user
    await cl.Message(content=msg_response).send()
