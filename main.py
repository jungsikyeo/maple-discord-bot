import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.getenv("STATIC_FOLDER")), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
