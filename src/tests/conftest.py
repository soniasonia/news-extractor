import sys
import os
import pytest
from os.path import dirname as d
from os.path import abspath

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

from api import create_app


os.environ["FLASK_ENV"] = "test"


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client
