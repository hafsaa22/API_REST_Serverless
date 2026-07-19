import json

def lambda_handler(event, context):
    """Exemple de fonction Lambda basique
    
    Arguments:
        event (dict): API Gateway Lambda Proxy Input Format
        context (object): Lambda Context runtime methods and attributes

    Returns:
        dict: API Gateway Lambda Proxy Output Format
    """

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world!",
            # "location": ip.text.replace("\n", "")
        }),
    }