import os
import pymysql
import json

# Read environment variables for MySQL
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

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

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'MySQL query executed successfully.',
                    'rows_preview': formatted,
                    'total_rows': len(rows)
                })
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
