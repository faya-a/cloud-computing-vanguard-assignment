import boto3

sqs = boto3.client("sqs")
queue_url = "https://sqs.region.amazonaws.com/account-id/my-queue"

# Send
sqs.send_message(QueueUrl=queue_url, MessageBody="Test message")

# Receive
response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
messages = response.get("Messages", [])
print(messages)
