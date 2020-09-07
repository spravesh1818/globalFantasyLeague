from sqlalchemy.orm import Session
import models,schemas



def get_teams(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db:Session,team:schemas.Team):
    db_team=models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db:Session,team_id:int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def create_user(db:Session,user:schemas.UserCreate):
    db_user=models.User(username=user.username,email=user.email,full_name=user.full_name,disabled=user.disabled,hashed_password=user.password,role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db:Session):
    return db.query(models.User).all()

def create_player(db:Session,player:schemas.Player):
    db_player=models.Player(name=player.name,nationality=player.nationality,kit_no=player.kit_no,dominant_foot=player.dominant_foot)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_player(db:Session,player_id:int):
    return db.query(models.Player).filter(models.Player.id==player_id).first()

def get_all_players(db:Session):
    return db.query(models.Player).all()