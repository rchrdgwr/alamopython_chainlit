import chainlit as cl

"""
 app_1: Basic structure of a chainlit app

 to run: chainlit run app_1.py
"""

# @cl.on_chat_start
#  - This is a decorator that identifies the function called
# when a new chat starts
#


@cl.on_chat_start
async def start():
    print("Chat started")
    msg = "Hello! I'm the Alamo Python chatbot. How can I help you today?"
    await cl.Message(content=msg).send()

# @ck.on_message
#  - This is a decorator that allows you to listen for messages in the chat
#  - It will trigger the function on_message whenever a new message is
# sent in the chat
#


@cl.on_message
async def on_message(message):
    print(f"Message received: {message}")
    await cl.Message(content=f"You said: {message.content}").send()
