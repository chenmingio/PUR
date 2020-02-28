import unittest
from config import TEMPLATE_FOLDER
from app.views import routes
from pprint import pprint


def test_get_project_report():
    data = routes.get_project_report("foo")
    pprint(data)
