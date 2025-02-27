import boto3
import pymysql
import os

# AWS and DB Config
s3 = boto3.client('s3')
bucket_name = os.environ['S3_BUCKET']
file_key = os.environ['FILE_KEY']

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def read_s3_file():
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = response['Body'].read().decode('utf-8')
    return data

def insert_into_rds(data):
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    with connection.cursor() as cursor:
        sql = "INSERT INTO my_table (data) VALUES (%s)"
        cursor.execute(sql, (data,))
        connection.commit()
    connection.close()

if __name__ == "__main__":
    data = read_s3_file()
    insert_into_rds(data)
    print("Data transferred successfully!")
