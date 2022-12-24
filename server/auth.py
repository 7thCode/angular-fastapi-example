# Copyright (c) 2019 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php

import json
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from server.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = json.load(open('config/default.json', 'r'))

SECRET = config['secret']

user = User(config['host'],config['db'], config['collection'])


def authenticate(name: str, password: str):
    result = None
    account = user.get_by_name(name)
    content = account["content"]
    if content["id"] == password:
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
        user.update_one({'user_id': user_id}, {'$set': {'content.access_token': access_token}})
        result = {"code": 0, 'access_token': access_token, 'token_type': 'bearer'}

    return result


def delete_token(user_id):
    result = {"code": -1, 'access_token': "", 'token_type': 'bearer'}
    if user_id is not None:
        user.update_one({'user_id': user_id}, {'$set': {'content.access_token': ""}})
        result = {"code": 0, 'access_token': "", 'token_type': 'bearer'}
    return result


async def user_from_access_token(token: str = Depends(oauth2_scheme)):
    result = None
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        if payload['token_type'] == "access_token":
            result = user.get_by_id(ObjectId(payload['user_id']))
    except Exception as e:
        pass
    return result


async def user_from_access_token_with_compare(token: str = Depends(oauth2_scheme)):
    result = None
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        if payload['token_type'] == 'access_token':
            account = user.get_by_id(ObjectId(payload['user_id']))
            content = account["content"]
            if content["access_token"] == token:
                result = account
    except Exception as e:
        pass
    return result
