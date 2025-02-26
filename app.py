import boto3
import pymysql
import os

s3 = boto3.client('s3')

def read_s3(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')


def push_to_rds(data, rds_config):
    try:
        connection = pymysql.connect(
            host=rds_config['host'],
            user=rds_config['user'],
            password=rds_config['password'],
            database=rds_config['database'],
            connect_timeout=5
        )
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO my_table (data) VALUES (%s)", (data,))
        connection.commit()
        print("Data pushed to RDS")
    except Exception as e:
        print("RDS connection failed, pushing to Glue instead")
        push_to_glue(data)


def push_to_glue(data):
    glue = boto3.client('glue')
    # Implement Glue logic here
    print("Data pushed to Glue Database")


if __name__ == '__main__':
    bucket = os.environ['S3_BUCKET']
    key = os.environ['S3_KEY']
    
    rds_config = {
        'host': os.environ['RDS_HOST'],
        'user': os.environ['RDS_USER'],
        'password': os.environ['RDS_PASSWORD'],
        'database': os.environ['RDS_DATABASE'],
    }

    data = read_s3(bucket, key)
    push_to_rds(data, rds_config)
