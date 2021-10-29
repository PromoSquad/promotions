# promotions

Project Promotions repo for NYU DevOps Fall 2021. A microservice that manages promotion information, leveraging technologies including Flask(Python), PostgreSQL, Travis CI and IBM Cloud.

## About

This project focuses on building a microservice that manages promotion information and applying various DevOps practices.

This is still in progress. Additional information, new features and more are being added into this repo.

For instructions for developers, please refer to [CONTRIBUTING.md](./CONTRIBUTING.md).

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
// Location: http://localhost:5000/promotions/1
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

## License

MIT, see [LICENSE](./LICENSE) file for details.

---

This repo is part of the DevOps course CSCI-GA.2820-001/002 at NYU taught by John Rofrano.
