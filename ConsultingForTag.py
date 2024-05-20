from google.cloud import bigquery

# Get credentials from environment variables
credential = r"C:\Users\rafae\Desktop\Coding challenge\new.json"
# Create BigQuery client
client = bigquery.Client.from_service_account_json(credential)

keyword = input('Enter the keyword you want to search: ')
# Query
query = """
    SELECT * FROM `teste1-423821.news.news19-05-24` 
    WHERE tags LIKE '%%%s%%'
""" % keyword

# Run the query
result = client.query(query)

for row in result:
    print("\n\n")
    print(f"Title: {row['title']}")
    print(f"Author: {row['author']}")
    print(f"Date: {row['date']}")
    print(f"Content: {row['content']}")
    print(f"Tags: {row['tags']}")
    print(f"Link: {row['link']}")
    print("\n\n")
