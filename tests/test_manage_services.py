import json
import os

def test_get_service_by_id(dynamodb_mock):
    from manage_services.app import lambda_handler
    
    table = dynamodb_mock.Table(os.environ["TABLE_NAME"])
    table.put_item(Item={
        "PK": "SERVICE#999", "SK": "DETAILS", "nom": "Service Existant", "description": "...", "categorie": "IT", "prix": "50"
    })
    
    event = {"pathParameters": {"id": "999"}, "httpMethod": "GET"}
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["nom"] == "Service Existant"

def test_delete_service(dynamodb_mock):
    from manage_services.app import lambda_handler
    
    table = dynamodb_mock.Table(os.environ["TABLE_NAME"])
    table.put_item(Item={"PK": "SERVICE#888", "SK": "DETAILS", "nom": "A Supprimer"})
    
    event = {"pathParameters": {"id": "888"}, "httpMethod": "DELETE"}
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 204
    items = table.scan()["Items"]
    assert len(items) == 0