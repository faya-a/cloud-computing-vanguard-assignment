from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT name, SUM(number) AS total
FROM `bigquery-public-data.usa_names.usa_1910_2013`
GROUP BY name
ORDER BY total DESC
LIMIT 10
"""

result = client.query(query)

for row in result:
    print(row.name, row.total)
