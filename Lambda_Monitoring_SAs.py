import boto3
import json

# Initialize the S3 and SNS clients
s3 = boto3.client('s3', region_name='ap-south-1')
sns = boto3.client('sns', region_name='ap-south-1')

def lambda_handler(event, context):
    # Get the bucket name and file key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the log file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    log_file_content = response['Body'].read().decode('utf-8')
    
    # Analyze the log file (this is just a placeholder - replace with your own log analysis)
    log_data = json.loads(log_file_content)
    if 'suspicious_activity' in log_data:
        # If suspicious activity is found, send an SNS notification
        sns.publish(
            TopicArn='arn:aws:sns:ap-south-1:295397358094:Nitish_SNS',
            Message='Suspicious activity detected in log file: ' + key,
            Subject='Suspicious Activity Detected'
        )
