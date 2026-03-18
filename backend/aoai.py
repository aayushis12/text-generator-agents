# pylint: disable=all
# from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# configure Azure OpenAI service client 
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_KEY']
)

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Hello!"}
#     ]
# )

# print(response.choices[0].message.content)

# deployment=os.environ['AZURE_OPENAI_DEPLOYMENT']

# add your completion code
prompt = "Complete the following: Once upon a time there was a mermaid"
messages = [{"role": "user", "content": prompt}]  
# make completion
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}, 
        {"role": "system", "content": "You are a helpful assistant that completes the user's prompt and generates a story for 4 year olds."}
    ]
)

# print response
print(completion.choices[0].message.content)
story = completion.choices[0].message.content

audio_response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",  # you can change voice later
    input=story
)

with open("story.mp3", "wb") as f:
    f.write(audio_response.content)
