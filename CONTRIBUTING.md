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

The default port for Flask service is `5000`, which is already mapped to host by our vagrant configuration. After starting the server, visit http://localhost:5000/ on your host.

### Start in dev mode

```bash
FLASK_ENV=development FLASK_APP=service:app flask run --host=0.0.0.0 --reload --debugger
```

This is with auto-reloader and debugger on. `--reload` enables auto-reloader so that your changes to the code will be applied automatically.

### Start in production mode

```bash
FLASK_APP=service:app flask run --host=0.0.0.0
```

### Run tests

Tests are written and put under folder `tests`. We use `nosetests` to run these tests and report coverages:

```bash
nosetests
```

## Model

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
