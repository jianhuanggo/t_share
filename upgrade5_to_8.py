import boto3
import time

# Initialize the RDS client
rds = boto3.client('rds')

# Variables
snapshot_name = "mydb-snapshot-5-7"
source_instance = "mydb-5-7"
new_instance = "mydb-8-0-temp"

def create_snapshot():
    print(f"Creating snapshot: {snapshot_name} from instance: {source_instance}")
    rds.create_db_snapshot(
        DBInstanceIdentifier=source_instance,
        DBSnapshotIdentifier=snapshot_name
    )

    print("Waiting for snapshot to be available...")
    waiter = rds.get_waiter('db_snapshot_available')
    waiter.wait(DBSnapshotIdentifier=snapshot_name)
    print("Snapshot is available.")

def restore_instance_from_snapshot():
    print(f"Restoring new instance: {new_instance} from snapshot: {snapshot_name}")
    rds.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=new_instance,
        DBSnapshotIdentifier=snapshot_name,
        Engine='mysql',
        EngineVersion='5.7',
        DBInstanceClass='db.m5.large'
    )

    print("Waiting for the new instance to be available...")
    waiter = rds.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=new_instance)
    print("New instance is available.")

def upgrade_instance_to_mysql_8_0():
    print(f"Upgrading instance: {new_instance} to MySQL 8.0")
    rds.modify_db_instance(
        DBInstanceIdentifier=new_instance,
        EngineVersion='8.0',
        AllowMajorVersionUpgrade=True,
        ApplyImmediately=True
    )

    print("Waiting for the upgrade to complete...")
    waiter = rds.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=new_instance)
    print("Upgrade to MySQL 8.0 completed.")

def automate_rds_replication_and_upgrade():
    create_snapshot()
    restore_instance_from_snapshot()
    upgrade_instance_to_mysql_8_0()
    print("RDS instance replicated and upgraded to MySQL 8.0 successfully.")

if __name__ == "__main__":
    automate_rds_replication_and_upgrade()
