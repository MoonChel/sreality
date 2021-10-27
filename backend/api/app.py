from fastapi import FastAPI, HTTPException
from .sreality.sreality import sreality
from .sreality.data_models import Result

app = FastAPI()


@app.get("/api", response_model=Result)
async def get_estates(url: str):
    if "www.sreality.cz" not in url:
        raise HTTPException("URL is not valid")

    estates = await sreality(url)

    return estates
