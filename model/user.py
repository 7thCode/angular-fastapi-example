# Copyright (c) 2022 7thCode.(http://seventh-code.com/)
# This software is released under the MIT License.
# opensource.org/licenses/mit-license.php
import abc
from bson.objectid import ObjectId
from pymongo import MongoClient


class User(metaclass=abc.ABCMeta):
    @abc.abstractmethod

    def __init__(self, host, db, collection):
        pass

    def create_one(self, username, password):
        pass

    def update_one(self, user_id, update):
        pass

    def delete_one(self, user_id):
        pass

    def find(self, query):
        pass

    def next(self):
        pass

    def get_by_name(self, username):
        pass

    def get_by_id(self, user_id):
        pass

    def set_token(self, user_id, access_token):
        pass
