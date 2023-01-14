# Copyright (c) 2022 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php

import hashlib
import json
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from model.user import User
from model.mongo import MongoUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = json.load(open('config/default.json', 'r'))

SECRET = config['secret']

user:User = MongoUser(config['host'], config['db'], config['collection'])

def create_user(username, password):
    return user.create_one(username, hashlib.sha256(password.encode()).hexdigest())


def update_user(user_id, update):
    return user.update_one(user_id, update)


def delete_user(user_id):
    return user.delete_one(user_id)


def find(query):
    return user.find(query)


def next():
    return user.next()


def authenticate(name: str, password: str):
    result = None
    account = user.get_by_name(name)
    if account["password"] == hashlib.sha256(password.encode()).hexdigest():
        result = account
    return result


def get_token(user_id):
    result = {"code": -1, 'access_token': "", 'token_type': 'bearer'}
    if user_id is not None:
        access_payload = {
            'token_type': 'access_token',
            'exp': datetime.utcnow() + timedelta(days=90),
            'user_id': str(user_id),
        }
        access_token = jwt.encode(access_payload, SECRET, algorithm='HS256')
        result = {"code": 0, 'access_token': access_token, 'token_type': 'bearer'}
    return result


def create_token(user_id):
    result = {"code": -1, 'access_token': "", 'token_type': 'bearer'}
    if user_id is not None:
        access_payload = {
            'token_type': 'access_token',
            'exp': datetime.utcnow() + timedelta(days=90),
            'user_id': str(user_id),
        }
        access_token = jwt.encode(access_payload, SECRET, algorithm='HS256')
        user.set_token(user_id, access_token)
        result = {"code": 0, 'access_token': access_token, 'token_type': 'bearer'}
    return result


def delete_token(user_id):
    result = {"code": -1, 'access_token': "", 'token_type': 'bearer'}
    if user_id is not None:
        user.set_token(user_id, "")
        result = {"code": 0, 'access_token': "", 'token_type': 'bearer'}
    return result


async def user_from_access_token(token: str = Depends(oauth2_scheme)):
    result = None
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        if payload['token_type'] == "access_token":
            result = user.get_by_id(payload['user_id'])
    except Exception as e:
        pass
    return result


async def user_from_access_token_with_compare(token: str = Depends(oauth2_scheme)):
    result = None
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        if payload['token_type'] == 'access_token':
            account = user.get_by_id(payload['user_id'])
            content = account["content"]
            if content["access_token"] == token:
                result = account
    except Exception as e:
        pass
    return result
