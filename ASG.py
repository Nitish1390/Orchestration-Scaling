import boto3, response, time
from ALB import create_load_balancer
# from ALB import instanced_id_list

#AWS Credentials and region
aws_access_key_id = 'AKIAYQKPEO5WBCOZGQGV'
aws_secret_access_key = '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'
region = 'ap-south-1'

resultALB = list(create_load_balancer())
target_grp_arn = resultALB[0]
instance_id = resultALB[1]

time.sleep(200)

#Create an Auto scaling group
def create_auto_scaling_group():
    autoscaling = boto3.client('autoscaling', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
    
# Create launch configuration
    autoscaling.create_launch_configuration(
        LaunchConfigurationName='Grp11LaunchTemplate',
        InstanceId=instance_id,
    )
    print("Lauch Template created successfully.")

# Create auto scaling group
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName='NitASG',
        LaunchConfigurationName='NitLaunchTemplate',
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        LoadBalancerTargetGroupConfigurations=[
        {
            'TargetGroupArn': target_grp_arn,
        },
    ],
        VPCZoneIdentifier='subnet-054d138c719f3f355, subnet-0ea24e054cba9cad2, subnet-0ea185273ead71a27',
    )
    print("ASG created successfully.")

# Create scale out policy
    scale_out_policy = autoscaling.put_scaling_policy(
        AutoScalingGroupName='NitASG',
        PolicyName='Nit_SCALE_OUT_POLICY',
        PolicyType='TargetTrackingScaling',
        TargetTrackingConfiguration={
            'PredefinedMetricSpecification': {
               'PredefinedMetricType': 'ASGAverageCPUUtilization',
            },
            'TargetValue': 20.0,
            # 'ScaleOutCooldown': 60,
            # 'ScaleInCooldown': 300,
        }
    )
    print("Scale OUT policy created successfully.")

# Create scale in policy
    # scale_in_policy = autoscaling.put_scaling_policy(
    #     AutoScalingGroupName='NitASG',
    #     PolicyName='Nit_SCALE_IN_POLICY',
    #     PolicyType='TargetTrackingScaling',
    #     TargetTrackingConfiguration={
    #         'PredefinedMetricSpecification': {
    #             'PredefinedMetricType': 'ASGAverageCPUUtilization',
    #         },
    #         'TargetValue': 10.0,
    #         # 'ScaleOutCooldown': 300,
    #         # 'ScaleInCooldown': 60,
    #     }
    # )
    # print("Scale IN policy created successfully.")

create_auto_scaling_group()
