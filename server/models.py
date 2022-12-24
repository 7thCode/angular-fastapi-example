# Copyright (c) 2019 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php

from pymongo import MongoClient

class User:
    client = None
    db = None
    collection = None

    def __init__(self, host,db,collection):
        with MongoClient(host, 27017) as client:
            self.client = client
            if self.client is not None:
                self.db = self.client[db]
                if self.db is not None:
                    self.collection = self.db[collection]

    def create(self):
        pass

    def get_by_name(self, username):
        account = None
        if self.collection is not None:
            account = self.collection.find_one({"username": username})
        return account

    def get_by_id(self, user_id):
        account = None
        if self.collection is not None:
            account = self.collection.find_one({"user_id": user_id})
        return account

    def update_one(self, filter, update):
        account = None
        if self.collection is not None:
            account = self.collection.update_one(filter, update)
        return account
