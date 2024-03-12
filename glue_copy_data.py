import boto3
from awsglue.utils import getResolvedOptions
import sys

# Retrieve arguments passed to the Glue job
args = getResolvedOptions(sys.argv, ['SOURCE_BUCKET', 'DESTINATION_BUCKET'])

source_bucket_name = args['SOURCE_BUCKET']
destination_bucket_name = args['DESTINATION_BUCKET']

s3 = boto3.client('s3')

def copy_objects(source_bucket, destination_bucket):
    # List objects in the source bucket
    response = s3.list_objects_v2(Bucket=source_bucket)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            copy_source = {
                'Bucket': source_bucket,
                'Key': obj['Key']
            }
            
            # Copy each object to the destination bucket
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=obj['Key'])
            print(f"Copied {obj['Key']} from {source_bucket} to {destination_bucket}")

# Call the function to start copying objects
copy_objects(source_bucket_name, destination_bucket_name)



import boto3

def assume_role(role_arn, session_name):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    credentials = assumed_role['Credentials']
    return credentials

def get_s3_client_with_assumed_role(credentials):
    return boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

def copy_objects(source_bucket, destination_bucket, object_key, s3_client):
    copy_source = {
        'Bucket': source_bucket,
        'Key': object_key
    }
    # Use the S3 client with assumed role credentials to copy the object
    s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=object_key)
    print(f"Copied {object_key} from {source_bucket} to {destination_bucket}")

# Parameters
source_bucket_name = 'source-bucket-name'
destination_bucket_name = 'destination-bucket-name'
object_key = 'example-object-key.txt'  # Specify the object key you want to copy
role_arn = 'arn:aws:iam::<destination-account-id>:role/<role-name>'  # Update with the actual role ARN
session_name = 'S3AccessSession'

# Main script
if __name__ == "__main__":
    # Assume the cross-account role and get temporary credentials
    credentials = assume_role(role_arn, session_name)

    # Create an S3 client using the assumed role's credentials
    s3_client = get_s3_client_with_assumed_role(credentials)


import boto3

def copy_to_bucket(source_bucket_name, target_bucket_name, object_name, source_profile_name, target_profile_name):
    # Create a session using the source account profile
    source_session = boto3.Session(profile_name=source_profile_name)
    s3_source = source_session.client('s3')
    
    # Create a session using the target account profile
    target_session = boto3.Session(profile_name=target_profile_name)
    s3_target = target_session.client('s3')
    
    # Copy object
    copy_source = {
        'Bucket': source_bucket_name,
        'Key': object_name
    }
    s3_target.copy(copy_source, target_bucket_name, object_name)
    print(f"Successfully copied {object_name} from {source_bucket_name} to {target_bucket_name}")

# Example usage
source_bucket = 'your-source-bucket-name'
target_bucket = 'your-target-bucket-name'
object_key = 'your-object-key'  # Example: 'foldername/filename.ext'
source_profile = 'sourceAWSProfile'  # Source AWS CLI profile name
target_profile = 'targetAWSProfile'  # Target AWS CLI profile name

copy_to_bucket(source_bucket, target_bucket, object_key, source_profile, target_profile)



    # Copy the object
    copy_objects(source_bucket_name, destination_bucket_name, object_key, s3_client)

