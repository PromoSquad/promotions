[![Run Python Tests](https://github.com/PromoSquad/promotions/actions/workflows/test.yml/badge.svg)](https://github.com/PromoSquad/promotions/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/PromoSquad/promotions/branch/main/graph/badge.svg?token=C8GU9IMZBE)](https://codecov.io/gh/PromoSquad/promotions)

# promotions

Project Promotions repo for NYU DevOps Fall 2021. A microservice that manages promotion information, leveraging technologies including Flask(Python), PostgreSQL, Travis CI and IBM Cloud.

## About

This project focuses on building a microservice that manages promotion information and applying various DevOps practices.

This is still in progress. Additional information, new features and more are being added into this repo.

For instructions for developers, please refer to [CONTRIBUTING.md](./CONTRIBUTING.md).

## Running on IBM Cloud

The service is deployed on IBM Cloud. You can visit it at [https://nyu-promotion-service-fall2103.us-south.cf.appdomain.cloud/](https://nyu-promotion-service-fall2103.us-south.cf.appdomain.cloud/).

## Run Service by Honcho

Make sure you have Python 3.8+ and [requirements.txt](./requirements.txt) installed. Then, run the following command:

```bash
PORT=8080 honcho start
```

## Service RESTful API Routes

### List all promotions

`GET /promotions`

Example response:

```jsonc
[
  {
    "id": 1,
    "product_id": 4,
    "name": "Amazing",
    "type": "coupon",
    "description": "Amazing $10 coupon for toasters",
    "meta": "{\"dollarsOff\":10}",
    "begin_date": "18-Nov-2018 (08:34:58.674035)",
    "end_date": null,
    "active": true
  }
  // ...
]
```

### List all active/inactive promotions

`GET /promotions?status=(active|inactive)`

Example response:

```jsonc
[
  {
    "id": 1,
    "product_id": 4,
    "name": "Amazing",
    "type": "coupon",
    "description": "Amazing $10 coupon for toasters",
    "meta": "{\"dollarsOff\":10}",
    "begin_date": "18-Nov-2018 (08:34:58.674035)",
    "end_date": null,
    "active": true
  }
  // ...
]
```

### List all promotions related to a product

`GET /promotions?productId=4`

Example response:

```jsonc
[
  {
    "id": 1,
    "product_id": 4,
    "name": "Amazing",
    "type": "coupon",
    "description": "Amazing $10 coupon for toasters",
    "meta": "{\"dollarsOff\":10}",
    "begin_date": "18-Nov-2018 (08:34:58.674035)",
    "end_date": null,
    "active": true
  }
  // ...
]
```

### Get one promotion

`GET /promotions/{id}`

Example response:

```jsonc
{
  "id": 1,
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true
}
```

### Create a promotion

`POST /promotions`

Example Request:

```jsonc
{
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true
}
```

Example Response:

```jsonc
// Location: http://localhost:8080/promotions/1
{
  "id": 1,
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true
}
```

### Update one promotion

`PUT /promotions/{id}`

Example Request:

```jsonc
{
  "id": 1,
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true
}
```

Example Response:

```jsonc
{
  "id": 1,
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true
}
```

### Activate/Deactivate one promotion

`PUT /promotions/{id}/(activate|deactivate)`

Example Response:

```jsonc
{
  "id": 1,
  "product_id": 4,
  "name": "Amazing",
  "type": "coupon",
  "description": "Amazing $10 coupon for toasters",
  "meta": "{\"dollarsOff\":10}",
  "begin_date": "18-Nov-2018 (08:34:58.674035)",
  "end_date": null,
  "active": true // or false
}
```

## License

MIT, see [LICENSE](./LICENSE) file for details.

---

This repo is part of the DevOps course CSCI-GA.2820-001/002 at NYU taught by John Rofrano.
