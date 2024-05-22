import boto3

def share_ami(source_ami_id, source_region, destination_account_id):
    # Initialize the boto3 client for the source AWS account
    ec2 = boto3.client('ec2', region_name=source_region)
    
    # Share the AMI with the destination AWS account
    response = ec2.modify_image_attribute(
        ImageId=source_ami_id,
        LaunchPermission={
            'Add': [{'UserId': destination_account_id}]
        }
    )
    
    return response

# Example usage
if __name__ == "__main__":
    source_ami_id = 'your-source-ami-id'
    source_region = 'source-ami-region'
    destination_account_id = 'destination-aws-account-id'

    response = share_ami(source_ami_id, source_region, destination_account_id)
    print("AMI shared successfully.")


import boto3

def copy_ami(source_ami_id, source_region, dest_region, dest_account_id):
    # Initialize the boto3 clients for both source and destination AWS accounts
    source_client = boto3.client('ec2', region_name=source_region)
    dest_client = boto3.client('ec2', region_name=dest_region)

    # Share the source AMI with the destination AWS account
    source_client.modify_image_attribute(
        ImageId=source_ami_id,
        LaunchPermission={
            'Add': [{'UserId': dest_account_id}]
        }
    )

    # Copy the AMI to the destination AWS account
    response = dest_client.copy_image(
        Name='Copied AMI',
        SourceImageId=source_ami_id,
        SourceRegion=source_region
    )

    return response['ImageId']

# Example usage
if __name__ == "__main__":
    source_ami_id = 'your-source-ami-id'
    source_region = 'source-ami-region'
    dest_region = 'destination-ami-region'
    dest_account_id = 'destination-aws-account-id'

    copied_ami_id = copy_ami(source_ami_id, source_region, dest_region, dest_account_id)
    print(f"Successfully copied AMI. New AMI ID: {copied_ami_id}")
