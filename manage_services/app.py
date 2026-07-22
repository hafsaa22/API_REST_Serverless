import json
import os
import boto3
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        service_id = event['pathParameters']['id']
        http_method = event['httpMethod']
        

        key = {
            'PK': f"SERVICE#{service_id}",
            'SK': "DETAILS"
        }
        
        response = table.get_item(Key=key)
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"erreur": f"Le service avec l'ID {service_id} n'existe pas."})
            }
            
        item_existant = response['Item']


        
        # --- GET : Consulter les détails ---
        if http_method == 'GET':
            return {
                "statusCode": 200,
                "body": json.dumps(item_existant, cls=DecimalEncoder)
            }
            
        # --- DELETE : Supprimer le service ---
        elif http_method == 'DELETE':
            table.delete_item(Key=key)
            return {
                "statusCode": 204,
                "body": ""
            }
            
        # --- PUT : Mettre à jour le service ---
        elif http_method == 'PUT':
            body = json.loads(event['body'])
            
            nom = body.get('nom', item_existant.get('nom'))
            description = body.get('description', item_existant.get('description'))
            categorie = body.get('categorie', item_existant.get('categorie'))
            prix = str(body.get('prix', item_existant.get('prix')))
            
            table.update_item(
                Key=key,
                UpdateExpression="SET nom = :n, description = :d, categorie = :c, prix = :p",
                ExpressionAttributeValues={
                    ':n': nom,
                    ':d': description,
                    ':c': categorie,
                    ':p': prix
                }
            )
            
            item_existant.update({'nom': nom, 'description': description, 'categorie': categorie, 'prix': prix})
            
            return {
                "statusCode": 200,
                "body": json.dumps(item_existant, cls=DecimalEncoder)
            }

    except Exception as e:
        print(f"Erreur interne: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"erreur": "Erreur interne du serveur."})
        }