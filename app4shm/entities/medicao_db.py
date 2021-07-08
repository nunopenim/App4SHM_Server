import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='root', server='localhost', database='db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

BASE = declarative_base()


def start() -> scoped_session:
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


class Medicao(BASE):
    __tablename__ = 'Medicao'
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.Float)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)
    username = db.Column(db.String(80))
    usernameGroup = db.Column(db.String(80))

    def __init__(self, identifier, t, x, y, z, username, usernameGroup):
        self.id = str(identifier)
        self.frequency = float(t)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.username = username
        self.usernameGroup = usernameGroup  # Foreign key do resultado


SESSION = start()

Medicao.__table__.create(checkfirst=True)

GROUPLOCK = threading.RLock()


def get_id():
    length = 0
    try:
        length = len(SESSION.query(Medicao).all())
    finally:
        SESSION.close()
        return length


def add_group(identification, t, x, y, z, username, usernameGroup):
    with GROUPLOCK:
        group = SESSION.query(Medicao).get(identification)
        if not group:
            group = Medicao(identification, t, x, y, z, username, usernameGroup)
        SESSION.merge(group)
        SESSION.commit()
