"""SQLAlchemy for NBAbet"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Table of users"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
 
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


class Teams(db.Model):
    """Table for NBA teams"""

    __tablename__ = 'teams'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    team_name = db.Column(
        db.Text,
        nullable=False,
    )

    image = db.Column(
        db.Text,
    )

