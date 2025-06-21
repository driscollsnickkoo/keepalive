import boto3
import json

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        key1 = event['key1']

        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:825765396866:QMPTableUpdateAlert',
            Message=f'NK Test sns from Lambda Message with key1 : {key1}',
            Subject='NK Test SNS from Lambda subject'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'messageId': response.get('MessageId'),
                'status': 'SNS notification sent'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'❌ NK lambda NK_helloworld_SNS Failed: {str(e)}')
        }