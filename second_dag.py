from airflow.sdk import dag, task
from datetime import datetime
import boto3

minio_endpoint = 'https://s3.cludus.org'  # Replace with your MinIO endpoint
minio_access_key = 'of2pi1oCEGjmeESS1Chk'           # Replace with your MinIO access key
minio_secret_key = 'M5BdAIdvjextADS1f0l3fFioEYBCndUBsyRPHCa6'

@dag(dag_id="my_dag", schedule="* * * * *", start_date=datetime(2025, 1, 1))
def my_dag():

    @task
    def my_task():
        s3_client = boto3.client(
            's3',
            endpoint_url=minio_endpoint,
            aws_access_key_id=minio_access_key,
            aws_secret_access_key=minio_secret_key,
            config=boto3.session.Config(signature_version='s3v4'),
            # For development or self-signed certificates, set verify=False
            verify=False
        )
        try:
            response = s3_client.list_buckets()
            print("Buckets in MinIO:")
            for bucket in response['Buckets']:
                print(f" - {bucket['Name']}")
        except Exception as e:
            print(f"Error connecting to MinIO or listing buckets: {e}")
        return 1

    @task
    def my_task2():
        print("my task 2")
        return 2

    @task
    def my_task3():
        print("my task 3")
        return 3

    my_task()
    my_task2()
    my_task3()

my_dag()
