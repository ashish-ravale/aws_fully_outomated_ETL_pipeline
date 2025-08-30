import boto3
import urllib.parse
import os

def lambda_handler(event, context):
    glue_client = boto3.client('glue')

    glue_job_name = os.environ.get("GLUE_JOB_NAME", "my-glue-job")

    # Extract bucket and key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    file_path = f"s3://{bucket}/{key}"

    try:
        response = glue_client.start_job_run(
            JobName=glue_job_name,
            Arguments={
                "--input_path": file_path,                 # single uploaded file
                "--output_path": f"s3://{bucket}/output/"  # output folder
            }
        )

        return {
            'statusCode': 200,
            'body': f"Started Glue job {glue_job_name} for file {file_path}, JobRunId: {response['JobRunId']}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error starting Glue job: {str(e)}"
        }
