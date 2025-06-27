import os
import pymysql

# Read environment variables
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

def lambda_handler(event, context):
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT t.RecordNumber, t.PalletID, t.SubmittedDate, t.BotProcessedDateTime, t.BotStatus, t.GrowerNumberUK FROM `qmp`.`T_Inspection_UK` t where t.BotStatus = 'Not Processed';")
            version = cursor.fetchone()
            print("Database version:", version)
        conn.close()
        return {
            "statusCode": 200,
            "body": f"Connected to MySQL, version: {version}"
        }
    except Exception as e:
        print("ERROR:", e)
        return {
            "statusCode": 500,
            "body": str(e)
        }
