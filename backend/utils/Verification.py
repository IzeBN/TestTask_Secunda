from fastapi import HTTPException, Header

from config import config

async def api_key(x_api_key: str = Header(...)):
    if x_api_key != config.api_token:
        raise HTTPException(401, "Invalid API Key")