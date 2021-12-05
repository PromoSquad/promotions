# Contributing

Promo Squad members, please refer to this guide for setting up development environment and also getting to know the model specifications.

## Vagrant

Vagrant is the VM development environment we're using in this class to develope our Flask services.

### Boot up

```bash
vagrant up
```

### SSH into the VM

```bash
vagrant ssh
```

### Halt

```bash
vagrant halt
```

### Destroy

```bash
vagrant destroy
```

## App

The port for our Flask service is `8080`, which is already mapped to host by our vagrant configuration. After starting the server, visit <http://localhost:8080/> on your host.

### Start in dev mode

```bash
FLASK_ENV=development FLASK_APP=service:app flask run --host=0.0.0.0 --port=8080 --reload --debugger
```

This is with auto-reloader and debugger on. `--reload` enables auto-reloader so that your changes to the code will be applied automatically.

### Start in production mode

```bash
PORT=8080 honcho start
```

### Run TDD tests

Tests are written and put under folder `tests`. We use `nosetests` to run these tests and report coverages:

```bash
nosetests
```

### Run BDD tests

Before you run the BDD tests, you should first start the service in dev or production mode at port 8080.

Then run the tests:

```bash
behave
```

## IBM Cloud

### Login and target resource

```bash
ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apikey.json -r us-south
ibmcloud target --cf -o yk2494@nyu.edu -s dev
```

### List Cloud Foundry apps

```bash
ibmcloud cf apps
```

### Generate `manifest.yml` for deployment

For dev environment:

```bash
APP_NAME=nyu-promotion-service-fall2103-dev python scripts/manifest.py

# or simply: (because this app name is the default)
python scripts/manifest.py
```

For prod environment:

```bash
APP_NAME=nyu-promotion-service-fall2103 python scripts/manifest.py
```

### Deploy

Make you have the right `manifest.yml` file existing in the root folder, then run:

```bash
ibmcloud cf push
```

## Model

> The implementation is at file [models.py](./service/models.py).

### Model: Promotion

| Column      | Type        | Remark                           |
| :---------- | :---------- | :------------------------------- |
| id          | int         | Primary Key                      |
| product_id  | int         | nullable, `null` means universal |
| name        | string (63) |                                  |
| type        | string (63) | "percentage", "coupon", "bogo"   |
| description | text        | nullable                         |
| meta        | json        | Promotion meta info              |
| begin_date  | timestamp   |                                  |
| end_date    | timestamp   | nullable                         |
| active      | boolean     |                                  |

For different promotion type, meta json is in different schema accordingly:

1. Percentage

   e.g.

   ```jsonc
   {
     "percentOff": 0.2 // 20% off discount
   }
   ```

2. coupon

   e.g.

   ```jsonc
   {
     "dollarsOff": 200.0 // 200 dollars off coupon
   }
   ```

3. BOGO

   e.g.

   ```jsonc
   {
     "buy": 1, // buy 1
     "get": 2 // get 1 for free
   }
   ```
