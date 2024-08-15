from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

# Create a thread
thread = client.beta.threads.create()

# Add a message to the thread
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hi!"
)

# Create a run using the assistant ID
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID
)

# Poll for run completion
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_status.status == "completed":
        break

# Retrieve the assistant's response
messages = client.beta.threads.messages.list(thread_id=thread.id)
assistant_response = messages.data[0].content[0].text.value
print(assistant_response)