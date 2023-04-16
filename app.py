import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
import json
from starlette.middleware.cors import CORSMiddleware
from models.models import BusinessTasks
import logging

load_dotenv()

chatGptAPIKey = os.getenv("CHATGPT_APIKEY")
openai.api_key = chatGptAPIKey

app = FastAPI(redoc_url=None, docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

messages_text = []


@app.post("/api/text2json")
def text2json(tasks: BusinessTasks):
    global messages_text  # не бейте за это не было время подключить postgres, а вообще в идеале тут ложится redis

    prompt = f"Write me a text UX in json format in {tasks.version} version design of the site with an approximate absolute " \
             "location and size in px of objects according to the business task. Send only json without any " \
             "additional text:"

    for task in tasks.tasks:
        prompt += task

    messages_text.append(
        {"role": "user", "content": prompt}
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_text,
        temperature=0.5,
    )

    try:
        response = json.loads(completion.choices[0]['message']['content'])
    except Exception as e:
        logger.error(e)
        messages_text.pop()
        response = {"error": completion.choices[0]['message']['content']}
        return response

    messages_text.append(
        {"role": "assistant", "content": completion.choices[0]['message']['content']}
    )

    return response


message_html = []


@app.post("/api/html2json")
def text2json(tasks: BusinessTasks):
    global message_html  # не бейте за это не было время подключить postgres, а вообще в идеале тут ложится redis

    prompt = "Write me a text UX design in FORMT JSON of the site with an approximate location and size in px of this " \
             f"objects that set you according to this body html document in a {tasks.version} version write only json without " \
             "additional text and info"

    for task in tasks.tasks:
        prompt += task

    message_html.append(
        {"role": "user", "content": prompt}
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_html,
        temperature=0.5,
    )

    try:
        response = json.loads(completion.choices[0]['message']['content'])
    except Exception as e:
        logger.error(e)
        message_html.pop()
        response = {"error": completion.choices[0]['message']['content']}
        return response

    message_html.append(
        {"role": "assistant", "content": completion.choices[0]['message']['content']}
    )

    return response
