import boto3

lambda_client = boto3.client("lambda")

response = lambda_client.invoke(
    FunctionName="my-lambda-function",
    Payload=b'{"event": "trigger"}'
)

print(response["StatusCode"])
