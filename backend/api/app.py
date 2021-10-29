from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .sreality.sreality import sreality
from .sreality.data_models import Result

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://werst.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/estates", response_model=Result)
async def get_estates(url: str):
    if "www.sreality.cz" not in url:
        raise HTTPException("URL is not valid")

    result = await sreality(url)

    return result
