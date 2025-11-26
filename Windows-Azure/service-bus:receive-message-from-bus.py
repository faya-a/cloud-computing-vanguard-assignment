from azure.servicebus import ServiceBusClient

conn_str = "AZURE_SERVICE_BUS_CONNECTION_STRING"
queue = "my-queue"

with ServiceBusClient.from_connection_string(conn_str) as sb:
    receiver = sb.get_queue_receiver(queue)
    with receiver:
        for msg in receiver.receive_messages(max_message_count=1, max_wait_time=5):
            print(msg)
            receiver.complete_message(msg)
