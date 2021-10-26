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

Running the App
Clone the project folder
"vagrant up" at the project folder root
"vagrant ssh" to ssh into the VM
"cd /vagrant/" to change directory to project folder root within the VM
"export FLASK_APP=service:app" to set the environment variable to run flask app
"flask run -h 0.0.0.0" to run the application
On host machine, visist: http://127.0.0.1:5000/
"nosetests" to run the tests
"coverage report -m" to see test coverage

## Setup

### Prerequisite Installation using Vagrant
The easiest way to use this is with Vagrant and VirtualBox. If you don't have this software the first step is download and install it. If you have an 2020 Apple Mac with the M1 chip, you should download Docker Desktop instead of VirtualBox. Here is what you need:
Download: Vagrant
Intel Download: VirtualBox
Apple M1 Download: Apple M1 Tech Preview
Install each of those. Then all you have to do is clone this repo and invoke vagrant:

### Using Vagrant and VirtualBox
```bash
Git clone https://github.com/DevOpsS21-Promotions/promotions.git
cd promotions
vagrant up
```
You can now ssh into the virtual machine and run the service and the test suite:
```bash
vagrant ssh
cd /vagrant
```
