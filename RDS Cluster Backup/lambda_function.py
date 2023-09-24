import boto3
import logging
from datetime import datetime

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a StreamHandler and set the log level to INFO
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a Formatter and set it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


# RDS cluster name
RDS_CLUSTER_NAME = 'hariom-rds'

# Variable for snapshot name
SNAPSHOT_PREFIX = 'hariom-rds-snapshot-'

def create_backup_with_tag():
    try:
        logger.info("create_backup_with_tag function started.")
        client = boto3.client('rds')

        # Get the current date and time for the tag and snapshot identifier
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%m-%d-%Y-%H-%M-%S")
        tag_name = current_date_time.strftime("%m-%d-%Y")

        # Create the RDS snapshot with the specified tag
        snapshot_identifier = f'{SNAPSHOT_PREFIX}{current_date_time_str}'
        response = client.create_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=snapshot_identifier,
            DBClusterIdentifier=RDS_CLUSTER_NAME,
            Tags=[
                {
                    'Key': 'backupon',
                    'Value': tag_name
                },
            ]
        )

        snapshot_id = response['DBClusterSnapshot']['DBClusterSnapshotIdentifier']
        logger.info(f"Snapshot ID: {snapshot_id}")

        return 'Snapshot created successfully.'
    except Exception as e:
        logger.error(f"An error occurred in create_backup_with_tag function: {e}")
        return 'Error creating snapshot.'

def lambda_handler(event, context):
    try:
        logger.info("Lambda execution started.")
        result = create_backup_with_tag()
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        logger.error(f"An error occurred in lambda_handler function: {e}")
        return {
            'statusCode': 500,
            'body': 'Error creating snapshots.'
        }
