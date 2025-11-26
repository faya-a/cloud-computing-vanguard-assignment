from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-sub")

response = subscriber.pull(
    subscription=subscription_path,
    max_messages=1
)

for msg in response.received_messages:
    print(msg.message.data)
    subscriber.acknowledge(subscription_path, [msg.ack_id])
