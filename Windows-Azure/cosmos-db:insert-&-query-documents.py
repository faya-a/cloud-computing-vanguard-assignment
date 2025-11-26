from azure.cosmos import CosmosClient

url = "COSMOS_DB_URL"
key = "COSMOS_DB_KEY"

client = CosmosClient(url, credential=key)
db = client.get_database_client("mydb")
container = db.get_container_client("items")

# Insert
container.create_item({
    "id": "1",
    "type": "demo",
    "value": "hello"
})

# Query
query = "SELECT * FROM c WHERE c.type='demo'"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

for item in items:
    print(item)
