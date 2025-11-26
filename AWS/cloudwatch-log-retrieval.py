import boto3

logs = boto3.client("logs")

response = logs.filter_log_events(
    logGroupName="/aws/lambda/my-lambda-function"
)

for event in response["events"]:
    print(event["message"])
