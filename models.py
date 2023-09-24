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
 
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    balance = db.Column(
        db.Float,
        default=1000.00,
    )

    bets = db.relationship('Ticket', backref='users')

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            username=username,
            password=hashed_pwd,     
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Game(db.Model):
    """Betting Odds/ Lines"""

    __tablename__ = 'games'

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

    home_ml_price = db.Column(
        db.Integer,
    )

    away_ml_price = db.Column(
        db.Integer,
    )

    home_PS = db.Column(
        db.Float,
    )

    away_PS = db.Column(
        db.Float,
    )

    home_PS_price = db.Column(
        db.Float,
    )

    away_PS_price = db.Column(
        db.Float,
    )

    over_under = db.Column(
        db.Text,
        default = 'OFF',
    )

    over_under_price = db.Column(
        db.Float,
        default = 0,
    )

    # game_date = db.Column(
    #     db.Text,
    # )

    # tipoff = db.Column(
    #     db.Text
    # )

    game_bet = db.relationship('Ticket', backref='games')

class Ticket(db.Model):
    """Parlay ticket table"""

    __tablename__ = "tickets"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )

    odds = db.Column(
        db.Integer,
        nullable=False,
    )

    amount_bet = db.Column(
        db.Float, 
        nullable=False
    )

    game_id = db.Column(
    db.Integer, 
    db.ForeignKey('games.id'),
    nullable=False,
    )

    ticket_user = db.relationship('User', backref='tickets')


class Sportsbook(db.Model):
    """Keep track of placed bets (Relationship Table)"""

    __tablename__ = "sportsbook"

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
        db.ForeignKey('tickets.id'), 
        nullable=False,
    )

    # sportsbook_user = db.relationship('User', backref='user_tickets')
    # sportsbook_game = db.relationship('Game', backref='game_tickets')