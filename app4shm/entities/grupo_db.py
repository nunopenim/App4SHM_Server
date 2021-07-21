# class Grupo:
# def __init__(self, ident, nome):
# self.ident = ident
# self.nome = nome

# how to run
# cd entities
# python
# from grupo_db import db
# db.create_all()
import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='app4shm', password='app4shm123', server='localhost', database='app4shm')
    #user='root', password='root', server='localhost', database='db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

BASE = declarative_base()


def start() -> scoped_session:
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], max_overflow=-1)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


class Grupo(BASE):
    __tablename__ = 'Grupo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, ident, nome):
        self.id = ident
        self.username = nome


SESSION = start()

Grupo.__table__.create(checkfirst=True)

GROUPLOCK = threading.RLock()


def get_id():
    length = 0
    try:
        length = len(SESSION.query(Grupo).all())
    finally:
        SESSION.close()
        return length


def add_group(identification, groupname):
    with GROUPLOCK:
        group = SESSION.query(Grupo).get(identification)
        if not group:
            group = Grupo(identification, groupname)
        SESSION.merge(group)
        SESSION.commit()


def showCol():
    with GROUPLOCK:
        return SESSION.query(Grupo).all()


def delCol(idDelete: int):
    with GROUPLOCK:
        SESSION.query(Grupo).filter(Grupo.id == idDelete).delete()
        SESSION.commit()
