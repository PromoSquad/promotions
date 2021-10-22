# Contributing

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
FLASK_APP=service FLASK_ENV=development flask run --host=0.0.0.0 --reload --debugger
```

This is with auto-reloader and debugger on. `--reload` enables auto-reloader so that your changes to the code will be applied automatically.

### Start in production mode

```bash
python ./main.py
```
