# RDS Snapshot Management Lambda

## Overview

This AWS Lambda function provides automated management of RDS cluster snapshots, allowing for tag-based creation and deletion. It is designed to simplify RDS snapshot management tasks by enabling users to define specific criteria for snapshot handling.

## Usage of Tags

This Lambda function uses tags to categorize RDS snapshots. Specifically, it utilizes a "backupon" tag with a date value to mark when a snapshot was created. This tag-based approach allows for the following:

- **Snapshot Creation**: When you trigger the "create_backup_with_tag" Lambda function, it creates a new RDS cluster snapshot and tags it with the current date. This makes it easy to identify when the snapshot was taken.

- **Snapshot Deletion**: The "delete_old_snapshots" Lambda function deletes snapshots that are older than a specified threshold (in this case, 7 days) by comparing the "backupon" tag value with the current date.

## Scheduled Automation

To fully utilize this Lambda function for snapshot management, you should set up scheduled automation using AWS CloudWatch Events or another scheduling mechanism. Here's how it works:

1. **Snapshot Creation**: Configure a scheduled event to trigger the "create_backup_with_tag" Lambda function at your desired interval (e.g., daily). This ensures that a new snapshot with the current date tag is created regularly.

2. **Snapshot Deletion**: Set up a scheduled event to trigger the "delete_old_snapshots" Lambda function at a frequency that aligns with your snapshot retention policy. In this case, the Lambda function deletes snapshots older than 7 days based on the "backupon" tag.

## Features

- **Automated Snapshot Creation**: Create RDS cluster snapshots with user-defined tags, enabling flexible scheduling and categorization.
- **Tag-Based Snapshot Deletion**: Delete outdated snapshots based on user-defined tags, providing fine-grained control over snapshot retention.
- **Customizable**: Easily configure the function by setting variables at the top of the script to match your AWS environment and tagging strategy.
- **Logging**: Utilizes built-in logging for tracking the execution and status of snapshot creation and deletion.

## Use Cases

- **Scheduled Backups**: Automatically create snapshots on a schedule and tag them for easy identification.
- **Snapshot Retention Policy**: Define retention policies based on tags, ensuring snapshots are retained only as long as needed.
- **Cost Optimization**: Avoid unnecessary costs by removing snapshots that are no longer needed, all based on specific tags.
- **Custom Tagging Strategy**: Implement a custom tagging strategy for snapshots to align with your organization's needs.

## Usage

1. **Create an IAM Role**: Before deploying the Lambda functions, create an IAM role with the necessary permissions. Ensure that the IAM role has permissions for actions such as `rds:CreateDBClusterSnapshot`, `rds:DeleteDBClusterSnapshot`, and `rds:DescribeDBClusterSnapshots`. Attach this IAM role to your Lambda functions during the deployment process.

2. **Deploy the Lambda Function**: Use AWS CloudFormation or deploy the Lambda function manually in the AWS Lambda console.

3. **Configure Variables (Optional)**: Customize the function by setting variables such as `SNAPSHOT_PREFIX` and `RDS_CLUSTER_NAME` to match your environment.

4. **Set Up Trigger**: Schedule the execution of both Lambda functions using AWS CloudWatch Events or other scheduling mechanisms. Configure "create_backup_with_tag" to run at your desired snapshot creation frequency and "delete_old_snapshots" to run at your retention policy frequency (e.g., day in 1 week).

5. **Monitor Logs**: Monitor CloudWatch Logs for detailed information on the execution of the Lambda functions.

6. **Adjust Retention Policy**: Modify the retention policy in the "delete_old_snapshots" Lambda function by changing the threshold (e.g., days) for snapshot deletion based on specific tags.

For detailed instructions on deploying and configuring the Lambda function, refer to the [official documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).

## Contributing

If you'd like to contribute to this project or have suggestions for improvements, please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. This means that you are free to use, modify, and distribute the code for any purpose, including commercial use. See the [LICENSE](LICENSE) file for details.


Made with love by Hari Om❤️.
