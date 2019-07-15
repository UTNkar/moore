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

## Getting Started - Virtual Environment

To get started with Project Moore, follow these instructions to set up a
development environment:

1. Install Python 3, at least version 3.5 or up.
2. Clone the repository.
3. Run `source ./source_me.sh` to create a virtual environment.
4. Run `pip install -r dev-requirements.txt`
5. Use `cd src` to enter the website directory.
6. Run `./manage.py migrate` to initialize the database.
7. Run `./manage.py createsuperuser` to create an admin user.

During development, you can run a test web server using `./manage.py
runserver`.

## Getting Started - Docker

If you can use Docker, there is an alternative way to get your development
environment all set up:

1. Clone the repository.
2. Run `docker-compose up` create and start the docker instance
3. Run `docker exec -it moore python src/manage.py migrate` to initialize the
database
4. Run `docker exec -it moore python src/ createsuperuser` to create an admin
user.

The Moore application is now available on `http://localhost:8000` and can be started
and stopped using `docker-compose up -d` and `docker-compose stop`.

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

These tests are run automatically using [Travis CI](https://travis-ci.org/).
If, however, you want to run these tests locally you can run the following
commands in the project root directory:

- `./src/manage.py test src` - to test with our Django test suites
- `flake8 src` - to run the flake8 style enforcer

## Translating

Project Moore intends to be multilingual. The web application is available in
both Swedish and English. Whenever any translatable text is added or changed it
should be translated using translation files.

*Within Project Moore we use American English.*

To create translations for an app:

1. `cd src/<appname>`
1. `../manage.py makemessages -l sv`
2. This will create or update the files under `src/<appname>/locale/`.
3. Use poedit (or your favourite tool -- please do not use a plain text editor
since those cannot handle all the subtleties) to fix the translations.
4. `../manage.py compilemessages`

## License

[AGPL-v2.0](LICENSE), unless a different, usually external, license is provided within a folder or file.
