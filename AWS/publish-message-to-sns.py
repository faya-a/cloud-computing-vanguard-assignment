import boto3

sns = boto3.client("sns")
topic_arn = "arn:aws:sns:region:account-id:topic-name"

sns.publish(
    TopicArn=topic_arn,
    Message="Demo event triggered",
    Subject="AWS Demo"
)
