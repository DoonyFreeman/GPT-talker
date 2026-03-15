from contextlib import asynccontextmanager

from fastapi import FastAPI, Body

from db import Base, engine, ChatRequest, get_user_requests
from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Database tables created.")
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/requests")
def get_my_requests():
    user_requests = get_user_requests(ip_address=user_ip_address)
    return "Here are your requests!"

@app.post("/requests")
def send_prompt(
    prompt: str = Body(embed=True,)
):
    answer = get_answer_from_gemini(prompt)
    return {"answer": answer}