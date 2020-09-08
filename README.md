# Gloabal Fantasy League

This is a experimental fantasy league.

## Installation

Clone this repository and install all the requirements.Preferably in a virtual environment.
After that run the server using command

```bash
uvicorn main:app --reload(optional)
```

## Database

The database is sqlite but feel free to connect to your own database by changing the database uri and supplying the username and password in the database.py file.
SqlAlchemy is used as the database orm.

## Authentication

Currently authentication is done using OAuth2 standard.A corresponding user table with role is defined.
Currently authorization is not implemented but gradually over time it will be implemented.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
