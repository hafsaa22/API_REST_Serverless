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


def test_update_service(dynamodb_mock):
    """Test la modification d'un service existant (PUT)."""
    from manage_services.app import lambda_handler
    
    # On prépare un service existant
    table = dynamodb_mock.Table(os.environ["TABLE_NAME"])
    table.put_item(Item={
        "PK": "SERVICE#777", "SK": "DETAILS", 
        "nom": "Ancien Nom", "description": "Ancienne desc", 
        "categorie": "IT", "prix": "100"
    })
    
    # On simule la requête de mise à jour
    event = {
        "pathParameters": {"id": "777"},
        "httpMethod": "PUT",
        "body": json.dumps({
            "nom": "Nouveau Nom", 
            "description": "Nouvelle desc", 
            "categorie": "IT", 
            "prix": 200
        })
    }
    
    # Exécution 
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    
    body = json.loads(response["body"])
    assert body["nom"] == "Nouveau Nom"
    assert body["prix"] == "200"


def test_get_service_not_found(dynamodb_mock):
    """Test le cas où l'ID n'existe pas dans la base (Erreur 404)."""
    from manage_services.app import lambda_handler
    
    # On interroge un ID fantôme
    event = {"pathParameters": {"id": "inexistant"}, "httpMethod": "GET"}
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert "n'existe pas" in body["erreur"]