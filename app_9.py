import chainlit as cl
from openai import OpenAI
import os
import json

from dotenv import load_dotenv

"""
 app_9: Simple AI Chatbot with additional Chainlit features

 to run: chainlit run app_9.py
"""

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# callback handlers


@cl.action_callback("icelandic")
async def on_icelandic(action):
    cl.user_session.set("language", "icelandic")
    await cl.Message(content="Skipt yfir í ensk").send()
    # Optionally remove the action button from the chatbot user interface
    # await action.remove()


@cl.action_callback("english")
async def on_english(action):
    cl.user_session.set("language", "english")
    await cl.Message(content="Changing to English").send()
    # Optionally remove the action button from the chatbot user interface
    # await action.remove()


# On Chat Start - used for pre-session setup #
@cl.on_chat_start
async def start():
    # set the language in the user session
    cl.user_session.set("language", "english")

    msg = "Hello! I'm the Alamo Python AI chatbot. Ask me a question?"
    await cl.Message(content=msg).send()
    # set up the action buttons
    actions = [
        cl.Action(
            name="english",
            value="english",
            description="Switch to English",
            payload={"language": "english"}  # Added payload
        ),
        cl.Action(
            name="icelandic", 
            value="icelandic", 
            description="Switch to Icelandic",
            payload={"language": "icelandic"}  # Added payload
        )
    ]
    # send the action buttons to the user
    await cl.Message(
        content="Welcome! Choose your preferred language:",
        actions=actions
        ).send()


# On Message - used for processing each user message #
@cl.on_message
async def main(message: cl.Message):
    language = cl.user_session.get("language", "english")
    messages = cl.chat_context.to_openai()

    system_prompt = f"""
        You are a helpful assistant who always responds in {language}.
        Be friendly and conversational while maintaining professionalism.
        If you're asked to switch languages, politely decline and continue in {language}.
    """

    messages.append({"role": "system", "content": system_prompt})

    messages.append({
        "role": "user", 
        "content": message.content
    })

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    msg_response = chat_completion.choices[0].message.content

    formatted_response = json.dumps(chat_completion.model_dump(), indent=2)

    # Print in console for debugging
    print("Raw API Response:", formatted_response)
    print("AI Response:", msg_response)

    # Send response to user
    await cl.Message(content=msg_response).send()
