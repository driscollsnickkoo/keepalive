import os
import pymysql
import boto3
import json

# Read environment variables for mysql
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']


# SNS config
sns_topic_arn = 'arn:aws:sns:eu-north-1:825765396866:sns_nktest'

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            connect_timeout=100
        )
        with conn.cursor() as cursor:
            query = """
                    SELECT t.RecordNumber, t.PalletID, t.SubmittedDate, t.BotProcessedDateTime, t.BotStatus, t.GrowerNumberUK 
                    FROM `qmp`.`T_Inspection_UK` t where t.BotStatus = 'Not Processed';
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            
        if rows:
            msg_lines = []
            for row in rows:
                line = f"Record: {row[0]}, PalletID: {row[1]}, Submitted: {row[2]}, BotStatus: {row[4]}"
                msg_lines.append(line)

            message = "\n".join(msg_lines)
            message = "NK is testing SNS"
            
            sns_response = sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject="NK test sns subject updated with eu-north-1 ",
                Message=f"Found NK {message}"
            )


            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'just mysql',
                    'messageId': sns_response.get('MessageId'),
                    'message': message
                    # ,
                    # 'rowsFound': len(rows)
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('No unprocessed records found.')
            }


        

    
    except Exception as e:
        print("ERROR:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }