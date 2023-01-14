# Copyright (c) 2022 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php

from bson.objectid import ObjectId
from pymongo import MongoClient

from model.user import User

class MongoUser(User):
    client = None
    db = None
    collection = None

    def __init__(self, host, db, collection):

        with MongoClient(host, 27017) as client:
            self.client = client
            if self.client is not None:
                self.db = self.client[db]
                if self.db is not None:
                    self.collection = self.db[collection]

    def create_one(self, username, password):
        account = None
        if self.collection is not None:
            already_exist = self.collection.find_one({"username": username})
            if already_exist is None:
                account = self.collection.insert_one({"user_id": ObjectId(), "username": username, "password": password, "level": 0, "access_token": ""})
        return account

    def update_one(self, user_id, update):
        account = None
        if self.collection is not None:
            account = self.collection.update_one({'user_id': user_id}, update)
        return account

    def delete_one(self, user_id):
        account = None
        if self.collection is not None:
            account = self.collection.delete_one({"user_id": user_id})
        return account

    def find(self, query):
        accounts = None
        if self.collection is not None:
            accounts = self.collection.find(filter=query)
        return accounts

    def next(self):
        cursor = None
        if self.collection is not None:
            cursor = self.collection.next()
        return cursor

    def get_by_name(self, username):
        account = None
        if self.collection is not None:
            account = self.collection.find_one({"username": username})
        return account

    def get_by_id(self, user_id):
        account = None
        if self.collection is not None:
            account = self.collection.find_one({"user_id": ObjectId(user_id)})
        return account

    def set_token(self, user_id, access_token):
        account = None
        if self.collection is not None:
            account = self.collection.update_one({'user_id': user_id}, {'$set': {'access_token': access_token}})
        return account
