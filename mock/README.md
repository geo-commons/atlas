# Mock API for Tables

With this mock API you can mock a REST API for the tables. Under the hood, json-server is used.
It simulates a real backend with filtering, pagination, so frontend development can proceed without a real API.

## Installation

Install dependencies once:

```bash
pnpm install
```

## Running the server

Start the mock API:

```bash
pnpm run start
```

The API will be available at http://localhost:4444/api

## Available endpoints

Examples (depending on what exists in `db.json`):

```http
GET /api/cities
GET /api/districts
GET /api/streets
GET /api/inhabitants
```

### Filtering

Filter by any field in the resource:

```http
GET /api/people?city=Amsterdam
GET /api/streets?district=Centrum
GET /api/inhabitants?city=Rotterdam&street=Coolsingel
```

### Pagination

- \_page → page number
- \_limit → items per page

Example:

```http
GET /api/inhabitants?_page=2&_limit=5
```

### Response format

List endpoints return structured data:

```json
{
  "results": [{ "id": 6, "firstName": "Eva", "lastName": "Bos" }],
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
