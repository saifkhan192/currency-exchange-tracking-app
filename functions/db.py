import os

import boto3

table_name = os.environ.get("TABLE_NAME", "currencies")
client = boto3.resource("dynamodb", region_name=os.environ["AWS_DEFAULT_REGION"])
currency_table = client.Table(table_name)
