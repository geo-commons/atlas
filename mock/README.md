# Mock API for Tables

With this mock API you can mock a REST API for the tables. Under the hood, json-server is used.
It simulates a real backend with filtering, pagination, so frontend development can proceed without a real API.

## Installation
Install dependencies once:
```bash
npm install
```

## Running the server
Start the mock API:
```bash
node server.js
```

The API will be available at http://localhost:4444/api

## Available endpoints
Examples (depending on what exists in `db.json`):

```bash
GET /api/cities
GET /api/districts
GET /api/streets
GET /api/inhabitants
```

### Filtering
Filter by any field in the resource:

```bash
GET /api/people?city=Amsterdam
GET /api/streets?district=Centrum
GET /api/inhabitants?city=Rotterdam&street=Coolsingel
```

### Pagination
```json
_page   → page number
_limit  → items per page
```

Example:
```bash
GET /api/inhabitants?_page=2&_limit=5
```

### Response format
List endpoints return structured data:

```bash
{
  "results": [
    { "id": 6, "firstName": "Eva", "lastName": "Bos" }
  ],
  "total": 24,
  "page": 2,
  "page_size": 5
}
```

Where:
- results → current page items
- total → total matching items
- page → current page number
- page_size → items per page