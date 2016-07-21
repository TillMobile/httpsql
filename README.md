```
Warning: This is an active WIP. Proceed with caution!
```

## API Quickstart

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

Install:
- `pip install https://github.com/TillMobile/httpsql/zipball/master/`

Start gunicorn (or your favorite WSGI server):
- `pip install gunicorn`
- `gunicorn httpsql.api:app`
- http://localhost:8000/

## Usage via HTTP(S)

### Schema
Retrieve the list of available collections and functions. Each collection lists its fields and their data types. Each function lists it's return type and parmaters.

GET `/`

```
{
  "functions": {
    "items_by_size": {
      "type": "item", 
      "parameters": {
        "t_size": "string"
      }
    }
  }, 
  "collections": {
    "item": {
      "attributes": {
        "read_only": false, 
        "is_pk": null, 
        "type": "map"
      }, 
      "description": {
        "read_only": false, 
        "is_pk": null, 
        "type": "string"
      }, 
      "id": {
        "read_only": false, 
        "is_pk": true, 
        "type": "number"
      }, 
      "name": {
        "read_only": false, 
        "is_pk": null, 
        "type": "string"
      }
    }
  }
}
```

### Insert
Insert records that conform to the defined schema.

PUT `/collection/{collection}/`

Single record body JSON
```
{
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}
```

Multiple record body JSON
```
[{
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}]
```

### Update
Update an existing record.

POST `/collection/{collection}/{pk}`

Single record body JSON
```
{
  "id" : 1, // optional
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}
```

### Delete
Delete an existing record.

DELETE `/collection/{collection}/{pk}`

### Retrieve by Primary Key
Retrieve a record from a collection by primary key.

GET `/collection/{collection}/{pk}`

Response JSON
```
{
  "id" : 1,
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}

```

### Retrieve by Query
Retrieve a list of records by query.

GET `/collection/{collection}/?{query}&order_by={order_by}&offset={offset}&limit={limit}`

Response JSON
```
[{
  "id" : 1,
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}]
```

Available query operators:
- `lt` (Less than)
- `lte` (Less than or equal)
- `gt` (Greater than)
- `gte` (Greater than or equal)
- `exact` (Equal)
- `contains` (Like)

Query examples:
- `name__exact=Shoe X`
- `attributes.weight__lte=5`
- `description__exact=name`

Order by examples:
- `id` order by id ascending
- `-id` order by id descending

Offset example:
- `1`

Limit example:
- `20`


### Row Count 
Retrieve the row count for the passed collection.

GET `/collection/{collection}/count?{query}`

Response JSON
```
{
  "count" : 1
}
```

### Retrieve by Function
Retrieve records by calling a function. Note: the parameters passed must match the function's schema. To function properly the return type of the function must match an a collection defined in the schema.  


GET `/function/{function}/?{parameters}`

Response JSON
```
[{
  "id" : 1,
  "name" : "Shoe X",
  "description" : "Awesome shoe",
  "attributes" : {
    "weight" : 0,
    "size" : "XL"
  }
}]
```

## Usage via client `client`

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


