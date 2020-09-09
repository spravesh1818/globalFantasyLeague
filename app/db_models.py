import sqlalchemy
from db import metadata


fantasy_team = sqlalchemy.Table(
    "fantasyteam",
    metadata,
    sqlalchemy.Column("fid", sqlalchemy.ForeignKey("users.id"), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
)

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

fantasy_players = sqlalchemy.Table(
    "fantasy_players",
    metadata,
    sqlalchemy.Column("fantasy_team_id", sqlalchemy.ForeignKey("fantasyteam.fid")),
    sqlalchemy.Column("player_id", sqlalchemy.ForeignKey("player.id")),
)

team = sqlalchemy.Table(
    "team",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("stadium", sqlalchemy.String, unique=True),
    sqlalchemy.Column("league_id", sqlalchemy.ForeignKey("league.id")),
)
