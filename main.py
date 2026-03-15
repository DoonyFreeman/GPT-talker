from fastapi import FastAPI


app = FastAPI()

@app.get("/requests")
def get_my_requests():
    return "Here are your requests!"