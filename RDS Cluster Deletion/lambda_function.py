import boto3
import logging
from datetime import datetime, timedelta
from pytz import timezone

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

def delete_old_snapshots():
    try:
        logger.info("Delete_old_snapshot function")
        client = boto3.client('rds')
        
        # Calculate the date 7 days ago
        filter_date = datetime.now(timezone("Asia/Kolkata")) - timedelta(days=7)
        tag_name = filter_date.strftime("%m-%d-%Y")
        logger.info(f"Filter date: {tag_name}")
        
        # Describe all DB cluster snapshots
        response = client.describe_db_cluster_snapshots()
         
        # Filter manual snapshots with the specified tag
        snapshots = response.get('DBClusterSnapshots', [])
        
        if not snapshots:
            logger.info("No snapshots found.")
            return 'No snapshots found.'
        
        snapshots_deleted = False 
        
        for snapshot in snapshots:
            S_type = snapshot['SnapshotType']
            if S_type == "manual" and 'TagList' in snapshot:
                for tag in snapshot['TagList']:
                    if tag.get('Key') == 'backupon' and tag.get('Value') == tag_name:
                        snapshot_id = snapshot['DBClusterSnapshotIdentifier']
                        try:
                            logger.info(f"Deleting snapshot: {snapshot_id}")
                            # print(snapshot_id)
                            client.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier=snapshot_id)
                            snapshots_deleted = True
                        except Exception as delete_error:
                            logger.error(f"Error deleting snapshot {snapshot_id}: {delete_error}")
        
        if snapshots_deleted:
            logger.info("Successfully deleted snapshots.")
            return 'Successfully deleted snapshots.'
        else:
            logger.info("No manual snapshots with the specified tag found.")
            return 'No manual snapshots with the specified tag found.'  
    except Exception as e:
        logger.error(f"An error occurred in delete_old_snapshots function: {e}")
        return None

def lambda_handler(event, context):
    try:
        logger.info("Lambda execution started.")        
        result = delete_old_snapshots()
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        logger.error(f"An error occurred in lambda_handler function: {e}")
        return {
            'statusCode': 500,
            'body': 'Error deleting snapshots.'
        }
