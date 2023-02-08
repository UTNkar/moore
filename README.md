# Project Moore

[![Build Status](https://travis-ci.org/UTNkar/moore.svg?branch=development)](https://travis-ci.org/UTNkar/moore)
[![Coverage Status](https://coveralls.io/repos/github/UTNkar/moore/badge.svg?branch=development)](https://coveralls.io/github/UTNkar/moore?branch=development)

Project Moore is a replacement for many of the [UTN](https://utn.se/) web
applications. Built using [Wagtail](https://wagtail.io/) and the [Django](https://www.djangoproject.com/) framework, Project
Moore intends to replace obfuscated custom applications. This is why this
project keeps a high regard to programming practice and documentation.

Any questions about the project can be send to the [UTN system
administrator](mailto:admin@utn.se).

Before contributing please read through our [contribution
guidelines](CONTRIBUTING.md).

To set up a local version of moore, use either Docker or a virtual environment (**recommended**).

## Getting Started - Docker

If you can use Docker, there is an alternative way to get your development
environment all set up:

1. Install [docker engine](https://docs.docker.com/engine/install/)
1. Install [docker compose](https://docs.docker.com/compose/install/).
   (On Ubuntu you can install `docker-compose` with `sudo apt install docker-compose`)
1. Clone the repository.
1. Copy `.env-template` to `.env` and fill in the environments.
1. Run `docker-compose up` create and start the docker instance
1. Run `docker exec -it moore python src/manage.py migrate` to initialize the
   database
1. Run `docker exec -it moore python src/manage.py createsuperuser` to create an admin
   user.

The Moore application is now available on `http://localhost:8000` and can be started using `docker-compose up -d` (the `-d` flag starts the instance in the background) and stopped `docker-compose stop`.

## Getting Started - Virtual Environment

To get started with Project Moore, follow these instructions to set up a
**development** environment:

1. Install Python 3, at least version 3.6 or up.
2. [Install postgresql](INSTALLING_POSTGRES.md)
3. Install the following python packages:
    - python3-venv
    - python3-dev
    - build-essential
    - libpq-dev
4. Clone the repository.
5. Copy the file `.env-template` and name the copy `.env`
6. Fill in the necessary variables in `.env`. `MELOS_URL` and `MELOS_ADMIN` are required. You might have to fill in some database credidentils. Check `src/moore/settings/base.py` for which default values are used if you don't specify and credidentials.
7. Run `source ./source_me.sh` to create a virtual environment.
8. Run `pip install --upgrade pip` to make sure that pip is running the latest version
9. Run `pip install -r dev-requirements.txt`
10. Use `cd src` to enter the website directory.
11. Run `./manage.py migrate` to initialize the database.
12. Run `./manage.py createsuperuser` to create an admin user.

During development, you can run a test web server using `./manage.py runserver`.

**IMPORTANT!** When running any command in moore, you must be in the virtual environment (a.k.a. `source source_me.sh`)

## Documentation

Documentation for Project Moore is split up into two parts. All documentation
regarding Project Moore's code base is located within the code. Like the rest
of the UTN infrastructure, a global overview of the application is documented
on [docs.utn.se](https://docs.utn.se/)

## Testing

All code in this repository is tested in two ways: we use [Django test
suites](https://docs.djangoproject.com/en/1.10/topics/testing/) and we run the
[flake8](http://flake8.pycqa.org/en/latest/) style enforcer. Together they can
promote clean and good code.

These tests are run automatically using Github Actions.
If, however, you want to run these tests locally you can run the following
commands in the project root directory:

-   `./src/manage.py test src` - to test with our Django test suites
-   `flake8 src` - to run the flake8 style enforcer

## Translating

Project Moore intends to be multilingual. The web application is available in
both Swedish and English. Whenever any translatable text is added or changed it
should be translated using translation files.

_Within Project Moore we use American English._

To create translations for an app:

1. `cd src/<appname>`
1. `../manage.py makemessages -l sv`
1. This will create or update the files under `src/<appname>/locale/`.
1. Use poedit (or your favourite tool -- please do not use a plain text editor
   since those cannot handle all the subtleties) to fix the translations.
1. `../manage.py compilemessages`

## Notes about the materialize framework

Project moore uses materialize as a css framework to get pre-built components.
The following components have been disabled in the `materialize.scss` file in the materialize app folder:

-   `navbar`

The reason for this is that they are not needed and are interfering with the code that we write. Keep this in mind
when updating or reinstalling materialize.

## Instagram feeds

Moore features a block that displays the latest image from instagram.
Using and developing it is a bit special so it has some separate instructions which can be read in its [README](/src/instagram/README.md)

## License

[AGPL-v3.0](LICENSE), unless a different, usually external, license is provided within a folder or file.
