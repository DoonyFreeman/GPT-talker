from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import Base, engine, get_user_requests, add_request_data
from gemini_client import GeminiClientError, get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Database tables created.")
    yield


app = FastAPI(lifespan=lifespan,
              title ="GPT-talker",
              description="A simple API that allows you to send prompts to Gemini and get answers. Also, you can get a history of your requests. The API is built using FastAPI and SQLAlchemy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return [
        {
            "id": item.id,
            "ip_address": item.ip_address,
            "prompt": item.prompt,
            "response": item.response,
        }
        for item in user_requests
    ]

@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True)
):
    normalized_prompt = prompt.strip()
    if not normalized_prompt:
        raise HTTPException(status_code=400, detail="Prompt must not be empty.")

    user_ip_address = request.client.host
    try:
        answer = get_answer_from_gemini(normalized_prompt)
    except GeminiClientError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Internal server error: {error}") from error
    add_request_data(
        ip_address=user_ip_address,
        prompt=normalized_prompt,
        response=answer
    )
    return {"answer": answer}
