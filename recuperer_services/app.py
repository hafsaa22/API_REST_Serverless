import json
import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
import base64


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
        scan_kwargs = {
            'Limit': 50,
            'FilterExpression': Attr('PK').begins_with('SERVICE#')
        }

        query_params = event.get('queryStringParameters')
        if query_params and 'next_token' in query_params:
            try:
                decoded_token = base64.b64decode(query_params['next_token']).decode('utf-8')
                scan_kwargs['ExclusiveStartKey'] = json.loads(decoded_token)
            except Exception:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"erreur": "Le paramètre next_token est invalide."})
                }

        response = table.scan(**scan_kwargs)
        services = response.get('Items', [])
        
        result = {
            "services": services,
            "count": len(services)
        }

        if 'LastEvaluatedKey' in response:
            last_key_json = json.dumps(response['LastEvaluatedKey'])
            next_token = base64.b64encode(last_key_json.encode('utf-8')).decode('utf-8')
            result['next_token'] = next_token

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result, cls=DecimalEncoder)
        }

    except Exception as e:
        print(f"Erreur interne: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"erreur": "Erreur interne lors de la récupération du catalogue."})
        }