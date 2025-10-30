import boto3
import os
from dotenv import load_dotenv

load_dotenv()

dynamo = boto3.resource(
    "dynamodb",
    region_name="eu-central-1",
    endpoint_url=os.getenv("DYNAMO_ENDPOINT", None),  # None → реальний AWS
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
)

FRIENDS_TABLE_NAME = "Friends"

existing_tables = dynamo.meta.client.list_tables()["TableNames"]
if FRIENDS_TABLE_NAME not in existing_tables:
    dynamo.create_table(
        TableName=FRIENDS_TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

friends_table = dynamo.Table(FRIENDS_TABLE_NAME)
