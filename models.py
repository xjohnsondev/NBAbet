"""SQLAlchemy for NBAbet"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


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

    balance = db.Column(
        db.Float,
        default=100.00,
    )

    bets = db.relationship('Game', backref='users')


class Game(db.Model):
    """Betting Odds/ Lines"""

    __tablename__ = 'odds'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    game_id = db.Column(
        db.Text,
        nullable=False,
    )

    home_team = db.Column(
        db.Text,
        nullable=False,
    )

    away_team = db.Column(
        db.Text,
        nullable=False,
    )

    home_h2h_price = db.Column(
        db.Integer,
        nullable=False,
    )

    away_h2h_price = db.Column(
        db.Integer,
        nullable=False,
    )

    home_PS = db.Column(
        db.Float,
        nullable=False,
    )

    away_PS = db.Column(
        db.Float,
        nullable=False,
    )

    home_PS_price = db.Column(
        db.Float,
        nullable=False,
    )

    away_PS_price = db.Column(
        db.Float,
        nullable=False,
    )

    bets = db.relationship('Bet', backref='game')


class Bet(db.Model):
    """Keep track of placed bets"""

    __tablename__ = "bets"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False,
    )

    game_id = db.Column(
        db.Integer, 
        db.ForeignKey('odds.id'), 
        nullable=False,
    )

    amount_bet = db.Column(
        db.Float, 
        nullable=False
    )

    user = db.relationship('User', backref='bets')
    game = db.relationship('Game', backref='bets')