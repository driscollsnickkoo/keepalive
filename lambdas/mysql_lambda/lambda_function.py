import boto3

sns_client = boto3.client('sns', region_name='eu-north-1')
sns_topic_arn = 'arn:aws:sns:eu-north-1:825765396866:sns_nktest'

def lambda_handler(event, context):
    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="SNS Test",
            Message="This is a test message from Lambda"
        )
        return {
            'statusCode': 200,
            'body': f'SNS message sent. MessageId: {response["MessageId"]}'
        }
    except Exception as e:
        print("SNS publish failed:", e)
        return {
            'statusCode': 500,
            'body': f'Failed to send SNS message: {str(e)}'
        }
