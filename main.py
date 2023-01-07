#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright (c) 2022 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php

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

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)
PUBLIC = "public"
PATH_PUBLIC = str(pathlib.Path(__file__).resolve().parent / PUBLIC)

app = FastAPI()

app.mount("/" + PUBLIC, StaticFiles(directory=PATH_PUBLIC), name=PUBLIC)


class NewUserParam(BaseModel):
    username: str
    password: str

class BaseParam(BaseModel):
    user_id: str

class UpdateParam(BaseParam):
    update: dict


class User(BaseModel):
    user_id: str
    username: str
    level: int


class UserResult(User):
    code: int


class ListResult(BaseModel):
    code: int
    value: list[User]


class TokenResult(BaseModel):
    code: int
    access_token: str
    token_type: str

@app.post("/account/create")
async def create(new_user: NewUserParam, operator=Depends(auth.user_from_access_token)):
    result = None
    if operator is not None:
        result = auth.create_user(new_user.username, new_user.password)
    return result


@app.put("/account/update")
async def update(update: UpdateParam, operator=Depends(auth.user_from_access_token)):
    result = None
    if operator is not None:
        result = auth.update_user(update.user_id, update.update)
    return result


@app.delete("/account/delete")
def delete(param: BaseParam, operator=Depends(auth.user_from_access_token)):
    result = None
    if operator is not None:
        result = auth.delete_user(param.user_id)
    return result


@app.get("/account/list", response_model=ListResult)
def find(query: str = "", option: str = ""):
    result = []
    q = json.loads(query)
    found = auth.find(q)
    try:
        doc = found.next()
        while found is not None:
            result.append(doc)
            doc = found.next()
    except StopIteration:
        pass
    return {'code': 0, 'value': result}


# Login
@app.post("/login", response_model=TokenResult)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_id = None
    user = auth.authenticate(form.username, form.password)
    if user is not None:
        user_id = user["user_id"]
    return auth.create_token(user_id)


# Logout
@app.delete("/logout", response_model=TokenResult)
async def logout(operator=Depends(auth.user_from_access_token_with_compare)):
    user_id = None
    if operator is not None:
        user_id = operator["user_id"]
    return auth.delete_token(user_id)


# getToken
@app.get("/get_token", response_model=TokenResult)
async def get_token(operator=Depends(auth.user_from_access_token_with_compare)):
    user_id = None
    if operator is not None:
        user_id = operator["user_id"]
    return auth.get_token(user_id)


# renewToken
@app.get("/renew_token", response_model=TokenResult)
async def renew_token(operator=Depends(auth.user_from_access_token_with_compare)):
    user_id = None
    if operator is not None:
        user_id = operator["user_id"]
    return auth.create_token(user_id)


#
@app.get("/self", response_model=UserResult)
async def self(operator=Depends(auth.user_from_access_token)):
    result = {"code": -1, "user_id": "", "username": ""}
    if operator is not None:
        result = {"code": 0, "level":operator["level"], "user_id": str(operator['user_id']), "username": str(operator['username'])}
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
