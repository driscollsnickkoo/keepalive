import boto3
import json

sns_client = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:eu-north-1:825765396866:sns_nktest'

def lambda_handler(event, context):
    try:
        # Log the incoming event for visibility
        print("Received event:", event)

        # Optional: format the message nicely
        message = json.dumps(event, indent=2)

        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='MySQL Query Result from Lambda'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'messageId': response.get('MessageId'),
                'status': 'SNS notification sent'
            })
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'nktest_sns failed: {str(e)}')
        }
