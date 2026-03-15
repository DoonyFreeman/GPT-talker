from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request

from db import Base, engine, ChatRequest, get_user_requests, add_request_data
from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Database tables created.")
    yield


app = FastAPI(lifespan=lifespan,
              title ="GPT-talker",
              description="A simple API that allows you to send prompts to Gemini and get answers. Also, you can get a history of your requests. The API is built using FastAPI and SQLAlchemy")

@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests

@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True)
):
    user_ip_address = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        response=answer
    )
    return {"answer": answer}