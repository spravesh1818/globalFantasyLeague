import sqlalchemy
from db import metadata

team = sqlalchemy.Table(
    "team",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("stadium", sqlalchemy.String, unique=True),
    sqlalchemy.Column("league_id", sqlalchemy.ForeignKey("league.id")),
)
