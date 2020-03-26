"""This is the raw script used for api_dynamodb_connector.py"""

import boto3
import decimal
import json
import transformer_model

from boto3.dynamodb.conditions import Key

CLIENT = boto3.resource('dynamodb')
TABLE_NAME = 'paycheck'
EMP_NO = 1614120
categories = ['incomes', 'deductions', 'attendances']

def _convert_decimals(items):
    def _decimal_default_proc(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            raise TypeError
    return json.dumps(items, default=_decimal_default_proc, ensure_ascii=False)
    

def lambda_handler(event, context):
    table = CLIENT.Table(TABLE_NAME)
    json_obj = table.query(
        KeyConditionExpression = Key('emp_no').eq(EMP_NO)
        # KeyConditionExpression = Key('emp_no').eq(EMP_NO) & Key('paid_date').gt('2019-12-01')
    )
    items = json_obj['Items']
    items = _convert_decimals(items)
    items = json.loads(items)
    
    transformer = transformer_model.TransformerModel(categories, items)
    transformer.get_timechart()
    json_response = json.dumps(transformer.response, ensure_ascii=False)
    print(json_response)
    return json_response
    # return 'Hello from lambda'