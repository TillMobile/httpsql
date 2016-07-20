## Quickstart

Create your `.env` file with a few variables:
- `DB_DATABASE`
- `DB_SCHEMA`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_CONNECTION_POOL_MIN`
- `DB_CONNECTION_POOL_MAX`
- `SCHEMA_AUTO_REFRESH_SECONDS` (Optional)
- `API_COLLECTION_ROW_LIMIT` (Optional)

Create and source a fresh virtualenv:
- `virtualenv venv`
- `source venv/bin/activate`

Install dependencies:
- `pip install -r requirements.txt`

Start gunicorn:
- `gunicorn api:app`
- http://localhost:8000/

## Using the client

```
from httpsql import client

# Make sure to set the HTTP_ENDPOINT env varible
# e.g. export HTTP_ENDPOINT=http://localhost:8000

# Retrieve filtered records
client.collection.table_or_view.filter(name__exact="Awesome")

# Retrieve count of filtered records
client.collection.table_or_view.count(id__gte=52)

# Paginate filtered records
client.collection.table_or_view.filter(limit=25, offset=25)

# Order filtered records
client.collection.table_or_view.filter(order_by="-id,name")

# Retrieve a single record by PK
client.collection.table_or_view.get(1)

# Insert record(s)
client.collection.table_or_view.insert([{
  "name" : "Nice"	
}])

# Update record
client.collection.table_or_view.update(1, {
	"name" : "Dang"
})

# Describe collection
client.collection.table_or_view.describe()

# Call a function
client.function.func_name.call(param1=1, param2="asd")

...

```