import sqlalchemy
from db import metadata

league = sqlalchemy.Table(
    "league",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("division", sqlalchemy.String),
)
