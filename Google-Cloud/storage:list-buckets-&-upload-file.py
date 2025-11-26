from google.cloud import storage

client = storage.Client()

# List buckets
buckets = list(client.list_buckets())
print([b.name for b in buckets])

# Upload file
bucket = client.bucket("my-bucket")
blob = bucket.blob("uploaded_file.txt")
blob.upload_from_filename("local_file.txt")
