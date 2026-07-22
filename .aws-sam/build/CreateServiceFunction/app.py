import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        if not event.get('body'):
            return {"statusCode": 400, "body": json.dumps({"erreur": "Le corps de la requête est vide."})}
            
        body = json.loads(event['body'])
        
        champs_requis = ['nom', 'description', 'categorie', 'prix']
        for champ in champs_requis:
            if champ not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"erreur": f"Le champ '{champ}' est obligatoire."})
                }
                
        service_id = str(uuid.uuid4())
        
        item = {
            'PK': f"SERVICE#{service_id}",
            'SK': "DETAILS",
            'id': service_id,
            'nom': body['nom'],
            'description': body['description'],
            'categorie': body['categorie'],
            'prix': str(body['prix'])
        }
        
        table.put_item(Item=item)
        
        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }
        
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"erreur": "Le payload fourni n'est pas un JSON valide."})
        }
    except Exception as e:
        print(f"Erreur interne: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"erreur": "Erreur interne du serveur."})
        }