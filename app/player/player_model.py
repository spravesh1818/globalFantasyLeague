import sqlalchemy
from db import metadata

player = sqlalchemy.Table(
    "player",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("nationality", sqlalchemy.String),
    sqlalchemy.Column("kit_no", sqlalchemy.String),
    sqlalchemy.Column("dominant_foot", sqlalchemy.String),
    sqlalchemy.Column("fantasy_price", sqlalchemy.Float),
    sqlalchemy.Column("team_id", sqlalchemy.ForeignKey("team.id")),
)
