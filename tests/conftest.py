import os
import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-north-1"
    os.environ["TABLE_NAME"] = "CatalogTableMock"

@pytest.fixture
def dynamodb_mock(aws_credentials):
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
        dynamodb.create_table(
            TableName=os.environ["TABLE_NAME"],
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield dynamodb