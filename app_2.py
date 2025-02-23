import chainlit as cl
from openai import OpenAI
import os
import json

from dotenv import load_dotenv

"""
 app_2: Simple AI Chatbot

 to run: chainlit run app_2.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

system_text = "You are a helpful and friendly chatbot."


# On Chat Start - used for pre-session setup #
@cl.on_chat_start
async def start():
    # create a chain

    msg = "Hello! I'm the Alamo Python AI chatbot. Ask me a question!"
    await cl.Message(content=msg).send()


# On Message - used for processing each user message #
@cl.on_message
async def main(message: cl.Message):
    # Call OpenAI API with system and user messages only (no history)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": message.content}
        ]
    )
    msg_response = chat_completion.choices[0].message.content

    formatted_response = json.dumps(chat_completion.model_dump(), indent=2)

    # Print in console for debugging
    print("Raw API Response:", formatted_response)
    print("")
    print("AI Response:", msg_response)

    # Send response to user
    await cl.Message(content=msg_response).send()
