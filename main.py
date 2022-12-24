#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pm2登録
# pm2 start result.py --name result --interpreter python3

import json
import pathlib

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from server import auth

config = json.load(open('config/default.json', 'r'))

app = FastAPI()


class Token(BaseModel):
    code: int
    access_token: str
    token_type: str


class User(BaseModel):
    code: int
    user_id: str
    username: str



PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)
PUBLIC = "public"
PATH_PUBLIC = str(pathlib.Path(__file__).resolve().parent / PUBLIC)

app.mount("/" + PUBLIC, StaticFiles(directory=PATH_PUBLIC), name=PUBLIC)

@app.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_id = None
    user = auth.authenticate(form.username, form.password)
    if user is not None:
        user_id = user["user_id"]
    return  auth.create_token(user_id)


@app.delete("/logout", response_model=Token)
async def renew_token(current_user: User = Depends( auth.user_from_access_token_with_compare)):
    user_id = None
    if current_user is not None:
        user_id = current_user["user_id"]
    return  auth.delete_token(user_id)


@app.get("/get_token", response_model=Token)
async def renew_token(current_user: User = Depends( auth.user_from_access_token_with_compare)):
    user_id = None
    if current_user is not None:
        user_id = current_user["user_id"]
    return  auth.get_token(user_id)


@app.get("/renew_token", response_model=Token)
async def renew_token(current_user: User = Depends( auth.user_from_access_token_with_compare)):
    user_id = None
    if current_user is not None:
        user_id = current_user["user_id"]
    return  auth.create_token(user_id)


@app.get("/self", response_model=User)
async def self(current_user: User = Depends( auth.user_from_access_token)):
    result = {"code": -1, "user_id": "", "username": ""}
    if current_user is not None:
        result = {"code": 0, "user_id": str(current_user['user_id']), "username": str(current_user['username'])}
    return result


@app.get('/')
def index():
    status_code = 200
    html_content = ""
    try:
        with open(PUBLIC + '/index.html', 'r') as file_index:
            html_content = file_index.read()
    except Exception as e:
        status_code = 500
        html_content = "Error"
    finally:
        return HTMLResponse(html_content, status_code=status_code)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, log_level="info")
