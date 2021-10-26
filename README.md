# promotions

Project Promotions repo for NYU DevOps Fall 2021

## Vagrant shutdown

If you are using Vagrant and VirtualBox, when you are done, you should exit the virtual machine and shut down the vm with:

```bash
 $ exit
 $ vagrant halt
```

If the VM is no longer needed you can remove it with:

```bash
  $ vagrant destroy
```

This repo is part of the DevOps course CSCI-GA.2820-001/002 at NYU taught by John Rofrano.

## Introduction

This lab is focusing on building an API which including the content related to the
promotion.

The project is still in process. Keeping adding information and new functions
about the promotion API.

## Prerequisite Installation for Intel Mac & PC

The easiest way to use this lab is with **Vagrant** and **VirtualBox**. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

```bash
    git clone https://github.com/nyu-devops/lab-flask-rest.git
    cd lab-flask-rest
    vagrant up
    vagrant ssh
    cd /vagrant
    FLASK_APP=service:app flask run -h 0.0.0.0
```

## Alternate install using VSCode and Docker

You can also develop in Docker containers using VSCode. This project contains a `.devcontainer` folder that will set up a Docker environment in VSCode for you. You will need the following:

- Docker Desktop for [Mac](https://docs.docker.com/docker-for-mac/install/) or [Windows](https://docs.docker.com/docker-for-windows/install/)
- Microsoft Visual Studio Code ([VSCode](https://code.visualstudio.com/download))
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) VSCode Extension

It is a good idea to add VSCode to your path so that you can invoke it from the command line. To do this, open VSCode and type `Shift+Command+P` on Mac or `Shift+Ctrl+P` on Windows to open the command palete and then search for "shell" and select the option **Shell Command: Install 'code' command in Path**. This will install VSCode in your path.

Then you can start your development environment up with:

```bash
    git clone https://github.com/nyu-devops/lab-flask-rest.git
    cd lab-flask-rest
    code .
```

The first time it will build the Docker image but after that it will just create a container and place you inside of it in your `/workspace` folder which actually contains the repo shared from your computer. It will also install all of the VSCode extensions needed for Python development.

If it does not automatically pronot you to open the project in a container, you can select the green icon at the bottom left of your VSCode UI and select: **Remote Containers: Reopen in Container**.

## Manually running the Tests

Run the tests using `nosetests`

```bash
  $ nosetests --with-spec --spec-color
```

**Notes:** the parameter flags `--with-spec --spec-color` add color so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red. The flag `--with-coverage` is automatcially specified in the `setup.cfg` file so that code coverage is included in the tests.

The Code Coverage tool runs with `nosetests` so to see how well your test cases exercise your code just run the report:

```bash
  $ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases.

To run the service use `flask run` (Press Ctrl+C to exit):

```bash
  $ FLASK_APP=service:app flask run -h 0.0.0.0
```

You must pass the parameters `-h 0.0.0.0` to have it listed on all network adapters to that the post can be forwarded by `vagrant` to your host computer so that you can open the web page in a local browser at: http://localhost:5000
