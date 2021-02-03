from flask_pymongo import PyMongo
from typing import List
from api.repository import validate_input


def insert_to_db(mongo: PyMongo, valid_data: List[dict]):
    mongo.db.articles.insert_many(valid_data)


def save_articles(mongo: PyMongo, data: List[dict]):
    valid_data = validate_input(data)
    insert_to_db(mongo, valid_data)
