from dotenv import load_dotenv
import discord
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
oai_client = OpenAI(api_key=OPENAI_KEY)
ASSISTANT_ID = os.getenv('ASSISTANT_ID')


def call_openai(question):
    completion = oai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": f"Respond like a Pirate to the following question:{question}"}
        ]
    )
    response = completion.choices[0].message.content
    print("OpenAI Response:", response)
    return response

# call_openai("how did you become a pirate?")


# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure that your bot can read message content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")
        message_content = message.content.split("$question")[1]
        print(f"Extracted question: {message_content}")
        response = call_openai(message_content)
        print(f"Assistant Response: {response}")
        await message.channel.send(response)

client.run(os.getenv('TOKEN'))