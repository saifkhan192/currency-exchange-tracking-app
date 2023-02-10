import json
import sys

sys.path.append("./functions")

from functions import handlers


def test_feed_currencies_handler():
    response = handlers.feed_currencies_handler({}, {})
    print(response)
    assert response["statusCode"] == 200


def test_get_currencies_handler():
    response = handlers.get_currencies_handler({}, {})
    print(response)
    data = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert "rates" in data
    assert "fluctuations" in data
    assert "USD" in data["rates"]
