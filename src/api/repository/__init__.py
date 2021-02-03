from api.data.news import Article
from typing import List


def validate_input(data: List[dict]):
    try:
        valid_data = []
        for item in data:
            article = Article(**item)
            valid_data.append(article.__dict__)
        return valid_data
    except TypeError as e:
        err = str(e).replace("__init__() got an ","")
        raise TypeError(f"Input json cannot be converted to list of Article objects ({err})")

