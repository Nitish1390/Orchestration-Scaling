import boto3, response

region = 'ap-south-1'
Name='Dynamic-Web-App-backend-Grp-7'
instance_type = 't2.micro'
image_id = 'ami-0f5ee92e2d63afc18'  # Replace with the desired AMI ID
security_group_ids = ['sg-0103a917e74448c29']
key_name = 'ec2_ramkumar'
user_data = """#!/bin/bash
    sudo apt update -y
    sudo apt install nginx -y
    sudo systemctl start nginx
    sudo systemctl enable nginx
    cd /home/ubuntu/
    git clone https://github.com/Ram4596/Dynamic_web_app.git
    cd /home/ubuntu/Grp11-web-app
    sudo cp index.html /var/www/html/
    sudo systemctl restart nginx"""

# Create an EC2 instance
def create_EC2_instance():
    ec2 = boto3.resource('ec2', region_name=region)

    response = ec2.create_instances(ImageId=image_id,
        InstanceType=instance_type,
        SecurityGroupIds=security_group_ids,
        TagSpecifications=[ { 'ResourceType': 'instance', 'Tags': [ { 'Key': 'Name', 'Value': 'Grp-7-web-app-backend' }, ] }, ],
        KeyName=key_name,
        UserData=user_data,
        MinCount=1,
        MaxCount=2)

    # Extract the instance ID
    instance_id_1 = response[0].id
    instance_id_2 = response[1].id

    # Print the instance ID
    print(f"EC2 instance {instance_id_1} has been created.")
    print(f"EC2 instance {instance_id_2} has been created.")
    
    return instance_id_1, instance_id_2


#create_EC2_instance()
