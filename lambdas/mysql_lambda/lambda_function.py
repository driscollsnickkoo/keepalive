import os
import pymysql
import json

# Read environment variables for mysql
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

# Uncomment below only if you want to test sns later
# import boto3
# sns_topic_arn = 'arn:aws:sns:eu-north-1:825765396866:sns_nktest'
# sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Attempt to connect to MySQL
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            connect_timeout=10
        )
        # Connection successful
        conn.close()
        return {
            'statusCode': 200,
            'body': json.dumps('MySQL connection successful.')
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error connecting to MySQL: {str(e)}')
        }
