import boto3

s3 = boto3.client("s3")

# List buckets
buckets = s3.list_buckets()
print([b["Name"] for b in buckets["Buckets"]])

# Upload a file
s3.upload_file("local_file.txt", "my-bucket-name", "uploaded_file.txt")
