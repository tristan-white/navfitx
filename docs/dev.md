# Development

Docs for developers.

# Architecture

NAVFITX is a Python app with a graphic user interface and a command line interface.

The backend uses [pydantic](https://pydantic.dev/docs/validation/latest/get-started/) to create models that represent performance evalution reports and to handle validation of data in reports. [SQLModel](https://sqlmodel.tiangolo.com/) is used to read/write reports to a database.

