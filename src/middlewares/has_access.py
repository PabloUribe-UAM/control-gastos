from datetime import datetime
from fastapi import HTTPException, Request
from src.utils.jwt import JWT


async def has_access(credentials: Request):
    try:
        token = credentials.headers.get("Authorization").split(" ")[1]
        payload = JWT.decode(token)

        date_time = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f")
        unix = int(date_time.timestamp())

        if payload['exp'] < unix:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return {
            "req": credentials,
            "payload": payload
        }
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")