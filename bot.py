from dotenv import load_dotenv
from openai import OpenAI
import discord
import time
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def create_thread():
    return openai_client.beta.threads.create()

def send_message(thread_id, assistant_id, content):
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    
    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)
    
    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

def conversation():
    thread = create_thread()    
    initial_prompt = "Hi!"    
    response = send_message(thread.id, ASSISTANT_ID, initial_prompt)    
    print(f"Assistant: {response}")    
    print("---")

# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))

@discord_client.event
async def on_message(message):
    thread = create_thread()            
    if message.author == discord_client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = send_message(thread.id, ASSISTANT_ID, message_content)    
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

discord_client.run(DISCORD_TOKEN)
