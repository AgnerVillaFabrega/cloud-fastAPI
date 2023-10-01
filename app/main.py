from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def docs():
    return RedirectResponse(url="/docs/")

