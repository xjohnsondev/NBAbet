from app import db
from models import User, Game, Ticket, Sportsbook


db.drop_all()
db.create_all()

admin = User.signup(username='admin', password='password', email='admin@admin.com')

db.session.add(admin)
db.session.commit()