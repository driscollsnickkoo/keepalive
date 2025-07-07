# nktest_mysql - new code 


import os
import pymysql
import json
import boto3

# Read environment variables for MySQL
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

# AWS Lambda client
# lambda_client = boto3.client('lambda')

sqs_client = boto3.client('sqs')
sqs_url = 'https://sqs.eu-north-1.amazonaws.com/825765396866/nktest_queue'
# arn:aws:sqs:eu-north-1:825765396866:nktest_queue



def lambda_handler(event, context):
    try:
        # Connect to MySQL
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            connect_timeout=10
        )

        with conn.cursor() as cursor:
            query = "SELECT * FROM T_Inspection_UK;"
            cursor.execute(query)
            rows = cursor.fetchall()
        
        conn.close()

        if rows:
            # Return only first 5 rows to keep message short
            preview = rows[:5]
            formatted = [str(row) for row in preview]

            sns_message = {
                'message': 'MySQL query executed successfully.',
                'rows_preview': formatted,
                'total_rows': len(rows)
            }

            # # Invoke nktest_sns Lambda asynchronously
            # response = lambda_client.invoke(
            #     FunctionName='nktest_sns',
            #     InvocationType='Event',  # Async
            #     Payload=json.dumps(sns_message).encode('utf-8')
            # )

            sqs_client.send_message(
                QueueUrl=sqs_url,
                MessageBody=json.dumps(sns_message)
            )

            print("SQS message sent")

            return {
                'statusCode': 200,
                'body': json.dumps(sns_message)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('Query ran but no rows found.')
            }

    except Exception as e:
        print("ERROR:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
