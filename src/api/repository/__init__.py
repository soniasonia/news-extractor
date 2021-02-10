from api.data.news import Article
from typing import List

err_generic = "Input json cannot be converted to list of Article objects"


def validate_input(data: List[dict]):
    try:
        valid_data = []
        for item in data:
            article = Article(**item)
            valid_data.append(article.__dict__)
        return valid_data
    except TypeError as e:
        err_details = str(e)
        if "__init__() got an unexpected" in err_details:
            err_details = err_details.replace("__init__() got an ", "")
        if "__init__() missing " in err_details:
            err_details = err_details.replace("__init__() ", "")
        err = f"{err_generic} ({err_details})"
        raise TypeError(err)
