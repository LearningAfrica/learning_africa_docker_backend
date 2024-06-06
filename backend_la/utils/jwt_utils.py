from jose import jwt 
from decouple import config
from datetime import datetime, timedelta

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = 'HS256'
EXPIRATION_TIME_IN_DAYS = 2

def encode_token(payload):
    expiration = datetime.utcnow() + timedelta(days=EXPIRATION_TIME_IN_DAYS)
    payload['exp'] = expiration
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])