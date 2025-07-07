import boto3
import json

sns_client = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:eu-north-1:825765396866:sns_nktest'

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = record['body']
        print("SQS message received:", message_body)

        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message_body,
            Subject='MySQL Query Result from Lambda'
        )

    return {
        'statusCode': 200,
        'body': json.dumps('All messages processed and sent to SNS.')
    }
