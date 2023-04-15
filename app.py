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
model_engine = "text-davinci-003"

app = FastAPI(redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/text2json")
def text2json(tasks: BusinessTasks):

    prompt = "Write me a text UX design of the site with an approximate location and size of objects according to the " \
             "business task in json format in desktop"
    for task in tasks.tasks:
        prompt += task

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return json.loads(completion.choices[0].text)
