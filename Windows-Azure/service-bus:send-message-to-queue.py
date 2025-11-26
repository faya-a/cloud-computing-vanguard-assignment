from azure.servicebus import ServiceBusClient, ServiceBusMessage

conn_str = "AZURE_SERVICE_BUS_CONNECTION_STRING"
queue = "my-queue"

with ServiceBusClient.from_connection_string(conn_str) as sb:
    sender = sb.get_queue_sender(queue)
    with sender:
        sender.send_messages(ServiceBusMessage("Test message"))
