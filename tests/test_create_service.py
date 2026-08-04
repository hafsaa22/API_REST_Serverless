import os
import json

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
    
    # Vérifications des critères d'acceptation 
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