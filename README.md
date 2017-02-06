# Project Moore

[![Build Status](https://travis-ci.org/UTNkar/moore.svg?branch=master)](https://travis-ci.org/UTNkar/moore)

Project Moore is a replacement for many of the [UTN](https://utn.se/) web
applications. Built using [Django](https://www.djangoproject.com/), Project
Moore intends to replace obfuscated custom applications. This is why this
project keeps a high regard to programming practice and documentation.

Any questions about the project can be send to the [UTN system
administrator](mailto:admin@utn.se).

Before contributing please read through our [contribution
guidelines](CONTRIBUTING.md).

## Getting Started

To get started with Project Moore, follow these instructions to set up a
development environment:

1. Install Python 3, at least version 3.5 or up.
2. Clone the repository.
3. Run `source ./source_me.sh` to create a virtual environment.
4. Run `pip install -r dev-requirements.txt`
5. Use `cd website` to enter the website directory.
6. Run `./migrate.py migrate` to initialize the database.
7. Run `./migrate.py creatsuperuser` to create an admin user.

During development, you can run a test web server using `./migrate.py
runserver`.

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

- `./website/manage.py test website` - to test with our Django test suites
- `flake8 website` - to run the flake8 style enforcer

## Translating

Project Moore intends to be multilingual. The web application is available in
both Swedish and English. Whenever any translatable text is added or changed it
should be translated using translation files.

*Within Project Moore we use American English.*

To create translations for an app:

1. `cd website/<appname>`
1. `../manage.py makemessages`
2. This will create or update the files under `website/<appname>/locale/`.
3. Use poedit (or your favourite tool -- please do not use a plain text editor
since those cannot handle all the subtleties) to fix the translations.
4. `../manage.py compilemessages`

## License

[AGPL-v2.0](LICENSE)
