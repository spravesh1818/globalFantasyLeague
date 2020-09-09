import sqlalchemy

from db import metadata

fantasy_team = sqlalchemy.Table(
    "fantasyteam",
    metadata,
    sqlalchemy.Column("fid", sqlalchemy.ForeignKey("users.id"), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
)


fantasy_players = sqlalchemy.Table(
    "fantasy_players",
    metadata,
    sqlalchemy.Column("fantasy_team_id", sqlalchemy.ForeignKey("fantasyteam.fid")),
    sqlalchemy.Column("player_id", sqlalchemy.ForeignKey("player.id")),
)
