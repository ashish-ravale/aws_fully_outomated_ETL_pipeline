# aws_fully_outomated_ETL_pipeline

Serverless ETL Pipeline with AWS Glue

This project is about building a serverless ETL pipeline on AWS. The idea is simple: whenever a new file gets uploaded to S3, a Glue job runs automatically, processes that file, and then I get notified about the job status.

I used different AWS services together to make this work without managing any servers.

🔗 How the Pipeline Works

Upload data to S3 – Whenever a new file is dropped in the S3 bucket, it kicks off the workflow.

Lambda trigger – A Lambda function listens for the S3 event and starts the Glue job.

Glue ETL job – The Glue job reads the uploaded file, applies transformations using PySpark, and writes the processed output back to another S3 location (or database if needed).

EventBridge – Tracks when the Glue job finishes (success or failure).

SNS notifications – I get an email about whether the ETL job succeeded or failed.

CloudWatch monitoring – Used for logs and debugging.

🛠️ AWS Services Used

S3 – Storage for raw and processed files

Lambda – To trigger Glue jobs automatically

Glue – For the actual ETL process (PySpark script)

EventBridge – To listen for Glue job completion events

SNS – To send me email notifications

CloudWatch – For monitoring and logging

📂 Project Files

lambda_function.py → Lambda function that triggers the Glue job

glue_script.py → PySpark script for data transformation in Glue

project_architecture.png → Architecture diagram (overall flow)

🚀 How to Try This Out

Upload a file into the input S3 bucket.

Lambda will catch the event and run the Glue job.

Glue processes the file and saves the result into the output location.

EventBridge + SNS will send you an email about whether the job passed or failed.

Check CloudWatch logs if something goes wrong.

📊 Why This Project

I built this to practice serverless data engineering and see how different AWS services fit together. It’s cost-effective, scalable, and works without needing to manage any servers.

Some use cases:

Automating data pipelines

Processing raw data for analytics

Getting real-time notifications when data is ready
