from azure.storage.blob import BlobServiceClient

connection_string = "AZURE_STORAGE_CONNECTION_STRING"
container_name = "my-container"

client = BlobServiceClient.from_connection_string(connection_string)
container = client.get_container_client(container_name)

# List blobs
for blob in container.list_blobs():
    print(blob.name)

# Upload file
with open("local_file.txt", "rb") as f:
    container.upload_blob("uploaded_file.txt", f, overwrite=True)
