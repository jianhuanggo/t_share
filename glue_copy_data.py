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
