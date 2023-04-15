import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
import json
from starlette.middleware.cors import CORSMiddleware
from models.models import BusinessTasks


load_dotenv()

chatGptAPIKey = os.getenv("CHATGPT_APIKEY")
openai.api_key = chatGptAPIKey

app = FastAPI(redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []


@app.post("/api/text2json")
def text2json(tasks: BusinessTasks):

    prompt = "Write me a text UX design of the site with an approximate location and size of objects according to the " \
             "business task in json format in desktop"
    for task in tasks.tasks:
        prompt += task

    messages.append(
        {"role": "user", "content": prompt}
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
    )

    messages.append(
        {"role": "assistant", "content": completion.choices[0]['message']['content']}
    )

    try:
        response = json.loads(completion.choices[0]['message']['content'])
    except Exception as e:
        response = {"error":completion.choices[0]['message']['content']}

    return response


