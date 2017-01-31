# Project Moore

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
regarding Project Moore's code base is located within the code. Like the rest of
the UTN infrastructure, a global overview of the application is documented on
[docs.utn.se](https://docs.utn.se/)


## Testing

Testing instructions for Project Moore will be updated soon...

## License

[AGPL-v2.0](LICENSE.md)
