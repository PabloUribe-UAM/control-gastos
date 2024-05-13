from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from os import getenv


class JWT:
    def encode(data, exp):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=exp)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, getenv('JWT_SECRET'), algorithm=getenv('JWT_ALG'))
        return encoded_jwt

    def decode(token):
        data = None
        try:
            data = jwt.decode(token, getenv('JWT_SECRET'), algorithms=[getenv('JWT_ALG')])
            return data
        except:
            raise HTTPException(400, {
                "status": 400,
                "message": "Invalid token"
            })