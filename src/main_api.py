import uuid
import httpx
from ML_Pipeline.utlis import regrex_code
from ML_Pipeline.db import UserQuery
from ML_Pipeline.infer import infer_message
from ML_Pipeline.dialog import process_message
from ML_Pipeline.utlis import client_id, get_client_query

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

answer_list = UserQuery(client_id)

chat_id = uuid.uuid4()

app = FastAPI()

app.mount("/static", StaticFiles(directory="../input/static"), name="static")

templates = Jinja2Templates(directory="../templates")


async def resolve_api(urls):
    async with httpx.AsyncClient() as client:
        response = await client.get(urls)
        data = response.json()
    # return response.text
    return data


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": client_id})


@app.post("/user")
async def read_query(request: Request):
    request_data_json = await request.json()
    message = regrex_code(request_data_json["message"])
    print(message,"regrex")
    api_urls = process_message(message, client_id, chat_id)
    print("url/prompt", api_urls)
    try:
        response = await resolve_api(api_urls)
        print(response, 'api response')
    except:
        # print(e)
        response = api_urls
        print(response, 'prompt response')

    return {"response": response, "originalMessage": request_data_json["message"]}


@app.get('/query', response_class=HTMLResponse)
def read_home(request: Request):
    queries = get_client_query()
    return templates.TemplateResponse("index.html", {"request": request, "query": queries})


# @app.get("/{message}")
# def read_test(message: str):
#     print(message)
#     response = infer_message(message)
#     print(response, '4')
#     return {"response": response}


@app.post("/test")
async def chatbot_test(request: Request):
    request_data_json = await request.json()
    message = "Will my access to foodwatch features be restricted if my status is 'Inactive'??"
    response = infer_message(message)
    print('test successful', response['intent']['name'])
    if response['intent']['name'] is not None:
        response = [{"text": "Hello! How can I help you today?"}]
        return {"response": response}
    response = [{"text": "Facing problem at server side.. please come back after some time."}]
    return {"response": response}


@app.get('/question/{number}')
def query(number):
    print("endpoint is called..")
    try:
        eval(number)
        number = int(number)
    except:
        number = str(number)
    print(number, "endpoint")
    response = answer_list.get_answers(number)
    print("get the response from api")
    return response[0]


@app.post('/add_answer')
def add_answer(question_no, answer: str):
    answer_list.add_answers(question_no, answer)
    return {"add": "OK"}


@app.get('/url')
async def url(urls):
    print(urls)
    url = 'http://127.0.0.1:8000/question/1'
    response = await resolve_api(url)
    print(response, "response")
# @app.get("/add")
# def read_item():
#     if add_prompt_reply():
#         return {"Done": "add the result!!!"}
#     else:
#         return {"Error": "db error is occurred"}
