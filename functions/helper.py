import json
from decimal import Decimal
from typing import List, Tuple, TypedDict
from urllib.request import urlopen
from xml.dom.minidom import parse

from boto3.dynamodb.conditions import Key
from db import currency_table


class Currency(TypedDict):
    currency_code: str
    rate: Decimal


def load_todays_currencies() -> Tuple[List[Currency], str]:
    """
    Downloads the remote xml feed, parses it and returns list of <currency_code, rate>
    """
    file = urlopen("http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    dom = parse(file)
    node_list = dom.getElementsByTagName("Cube")
    currencies = []
    date = ""
    for node in node_list:
        if node.hasAttribute("time"):
            date = node.attributes["time"].value
        if node.hasAttribute("currency"):
            item = {
                "currency_code": node.attributes["currency"].value,
                "rate": Decimal(node.attributes["rate"].value),
            }
            currencies.append(item)

    return currencies, date


def feed_currencies():
    """
    Get list of currencies, and insert into DynamoDB (avoid duplication for same date)
    """
    currencies, date = load_todays_currencies()
    any_currency = currencies[0]["currency_code"]

    filters = Key("currency_code").eq(any_currency) & Key("date").eq(date)
    result = currency_table.query(KeyConditionExpression=filters)

    if result["Count"] == 0:
        with currency_table.batch_writer() as batch:
            for currency in currencies:
                item = {
                    "currency_code": currency["currency_code"],
                    "rate": currency["rate"],
                    "date": date,
                }
                batch.put_item(Item=item)

    print("feed_currencies() executed")


def fetch_from_table(keyConditionExpression):
    """
    Execute the provided filters on currency table and return the result
    """
    params = dict(
        IndexName="date-index",  # use Global Secondary Index
        KeyConditionExpression=keyConditionExpression,
        Limit=50,
    )
    response = currency_table.query(**params)
    rows = response["Items"]
    while "LastEvaluatedKey" in response:
        params["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = currency_table.query(**params)
        rows.extend(response["Items"])
    return rows


def response(statusCode, body):
    return {
        "statusCode": statusCode,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
