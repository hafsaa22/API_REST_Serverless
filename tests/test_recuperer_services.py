import json
import os

def test_get_all_services(dynamodb_mock):
    from recuperer_services.app import lambda_handler
    
    # On insère un faux service dans la base de données mockée
    table = dynamodb_mock.Table(os.environ["TABLE_NAME"])
    table.put_item(Item={
        "PK": "SERVICE#12345",
        "SK": "DETAILS",
        "nom": "Test Unitaire",
        "prix": "99"
    })
    
    # On appelle notre Lambda
    event = {"queryStringParameters": None}
    response = lambda_handler(event, None)
    
    # On vérifie les résultats
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 1
    assert body["services"][0]["nom"] == "Test Unitaire"