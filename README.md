# Bulker: RESTful service for a potential web-version of a table game

![Bulker Logo](./docs/img/bulker_300.png)

![CI/CD Workflow](https://github.com/Belstowe/bulker-server-django/actions/workflows/ci.yml/badge.svg?event=push)

## Table of Contents

* [Background](#background)
* [Development stack](#development-stack)
* [Contract](#development-stack)
* [Deployment](#deployment)
  * [Using Docker Compose](#using-docker-compose)
  * [Using Helm](#using-helm)

## Background

Bulker is built as a back-end for potential web adaptation of a table game called Bunker.

## Development stack

* Python 3.10;
* Django + Django REST Framework;
* Gunicorn + Nginx;
* MongoDB;
* Docker;
* Kubernetes + Helm.

## Contract

There is a contract which Bulker is based on. You may check it out [here](./docs/contract/). It's built upon OpenAPI 3.0.3 specification.

Contract implementation list:

* Players' general info:
  * ~~Players: get info, add a new record, clear all records~~
  * ~~Player {id}: get info, update the record, delete the record~~
* Votes' mechanics:
  * ~~Vote of player {id}: get, cancel~~
  * ~~Votes for player {id}: get vote spree, clear all votes~~
  * ~~Vote of player {subjectid} for player {objectid}: give a vote (with clearing the previous one)~~
  * ~~Votes: clear all votes~~
  * ~~Did all players vote?~~
* Event: get a new event *(events are formed by parsing .yml)*
* Conditions *(formed by parsing .yml)*:
    * Conditions: get details
    * Condition {codename}: get details, update, randomize
* Players' traits *(formed by parsing .yml)*:
    * Players' traits: get names
    * Traits of player {id}: get details
    * Trait {codename} of player {id}: get details, update, randomize

## Deployment

### Using Docker Compose

You can deploy a fixed num nodes' cluster by using Docker Compose:

```bash
$ python confenv.py
$ docker-compose build
$ docker-compose up
```

You need to configure env variables only once.
If you didn't change the project, you don't need to build cluster as well.

### Using Helm

```bash
$ helm install my-release
          --set db_user={db_user}
          --set db_password={db_password}
          --set db_host={db_host}
          --set-string db_port={db_port}
          --set db_name={db_name}
          --set host={appengine_host}
          --set secret_key={django_secret_key}
          ./charts
```

Note that you're required to have MongoDB service deployed already.