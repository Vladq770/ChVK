import os
from dotenv import load_dotenv
from jwt import encode

load_dotenv()

JWT_SECRET_KEY1 = os.getenv("JWT_SECRET_KEY1")
JWT_SECRET_KEY2 = os.getenv("JWT_SECRET_KEY2")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")



def get_tokens(id, last_login):
    token = {
        'access_token': encode({"id": id}, f"{JWT_SECRET_KEY1}{last_login}", algorithm=JWT_ALGORITHM),
        'refresh_token': encode({"id": id}, f"{JWT_SECRET_KEY2}{last_login}", algorithm=JWT_ALGORITHM)
    }
    return token
