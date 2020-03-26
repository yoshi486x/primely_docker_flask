import boto3
import decimal
import json


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)
    json_reader = json_object['Body'].read()
    json_dict = json.loads(json_reader, parse_float=decimal.Decimal)
    
    table = dynamodb.Table('paycheck')
    table.put_item(Item=json_dict)
    
    # print(bucket)
    # print(json_file_name)
    # print(str(event))
    return 'Hello from Lambda'    
