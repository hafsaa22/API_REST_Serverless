import os
import json
import pytest
import boto3
from moto import mock_aws

# --- CONFIGURATION DU FAUX ENVIRONNEMENT AWS ---
@pytest.fixture
def aws_credentials():
    """Crée de fausses clés AWS pour être sûr de ne pas toucher au vrai Cloud."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-north-1"
    os.environ["TABLE_NAME"] = "CatalogTableMock"

@pytest.fixture
def dynamodb_mock(aws_credentials):
    """Démarre le faux DynamoDB et crée la table vide en mémoire."""
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

# --- LES TESTS MÉTIERS ---
def test_create_service_success(dynamodb_mock):
    """Test le scénario nominal : création réussie d'un service."""
    from create_service.app import lambda_handler
    
    # On simule la requête entrante d'API Gateway
    event = {
        "body": json.dumps({
            "nom": "Audit Backend",
            "description": "Analyse d'architecture Serverless",
            "categorie": "IT",
            "prix": 1500
        })
    }
    
    # Exécution de la fonction
    response = lambda_handler(event, None)
    
    # Vérifications des critères d'acceptation (Asserts)
    assert response["statusCode"] == 201
    assert "Access-Control-Allow-Origin" in response["headers"]
    
    body = json.loads(response["body"])
    assert body["nom"] == "Audit Backend"
    assert "id" in body
    
    # Vérification directe dans la fausse base de données
    table = dynamodb_mock.Table(os.environ["TABLE_NAME"])
    items = table.scan()["Items"]
    assert len(items) == 1
    assert items[0]["nom"] == "Audit Backend"

def test_create_service_missing_field(dynamodb_mock):
    """Test le scénario d'erreur : champ manquant."""
    from create_service.app import lambda_handler
    
    event = {
        "body": json.dumps({
            "nom": "Audit Backend",
            # "description" est manquant
            "categorie": "IT",
            "prix": 1500
        })
    }
    
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "obligatoire" in body["erreur"]