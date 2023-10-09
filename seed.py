from app import db
from models import User, Game, Ticket, Counter

db.drop_all()
db.create_all()

admin = User.signup(username='admin', password='password', email='admin@admin.com')

db.session.add(admin)
db.session.commit()

g1 = Game(game_id="fd55db2fa9ee5be1f108be5151e2ecb0", start_time="Oct 24, 2023 @ 04:30 PM", day="Oct 24", home_team="Denver Nuggets", away_team="Los Angeles Lakers", home_ml_price=-205, away_ml_price=170, home_PS=-5, away_PS=5, home_PS_price=-110, away_PS_price=-110, over_under=227.0, over_under_price=-110)
g2 = Game(game_id="a44e83dd9ce3f2317ec644774daa859b", start_time="Oct 24, 2023 @ 07:00 PM", day="Oct 24", home_team="Golden State Warriors", away_team="Phoenix Suns", home_ml_price=-110, away_ml_price=-110, home_PS=-1, away_PS=1, home_PS_price=-105, away_PS_price=-115, over_under=232.5, over_under_price=-110)
g3 = Game(game_id="be1ee8db7ba20de87a087e8851f9b2f5", start_time="Oct 25, 2023 @ 04:00 PM", day="Oct 25", home_team="Charlotte Hornets", away_team="Atlanta Hawks", home_ml_price=-125, away_ml_price=105, home_PS=-1.5, away_PS=1.5, home_PS_price=-110, away_PS_price=-110, over_under_price=0)
g4 = Game(game_id="866b0f885ae4bebcabf5a6d57eb4064a", start_time="Oct 25, 2023 @ 04:00 PM", day="Oct 25", home_team="New York Knicks", away_team="Boston Celtics", home_ml_price=-135, away_ml_price=114, home_PS=-2.5, away_PS=2.5, home_PS_price=-110, away_PS_price=-110, over_under_price=0)
g5 = Game(game_id="13898382e266df26f137ea596fd51666", start_time="Oct 25, 2023 @ 04:00 PM", day="Oct 25", home_team="Orlando Magic", away_team="Houston Rockets", home_ml_price=136, away_ml_price=-162, home_PS=3.5, away_PS=-3.5, home_PS_price=-110, away_PS_price=-110, over_under_price=0)
g6 = Game(game_id="27ba27b22fe22e75d917a4bf9c7d0b1c", start_time="Oct 25, 2023 @ 04:00 PM", day="Oct 25", home_team="Indiana Pacers", away_team="Washington Wizards", home_ml_price=-325, away_ml_price=260, home_PS=-7.5, away_PS=7.5, home_PS_price=-110, away_PS_price=-110, over_under_price=0)
g7 = Game(game_id="a1cd3feca01c061a891025f73ef39b22", start_time="Oct 25, 2023 @ 04:30 PM", day="Oct 25", home_team="Brooklyn Nets", away_team="Cleveland Cavaliers", home_ml_price=105, away_ml_price=-125, home_PS=1.5, away_PS=-1.5, home_PS_price=-110, away_PS_price=-110, over_under_price=0)
g8 = Game(game_id="06ae6d0547da80d7854c003842247b43", start_time="Oct 25, 2023 @ 04:30 PM", day="Oct 25", home_team="Miami Heat", away_team="Detroit Pistons", home_ml_price=340, away_ml_price=-440, home_PS=9.5, away_PS=-9.5, home_PS_price=-115, away_PS_price=-105, over_under_price=0)

db.session.add_all([g1,g2,g3,g4,g5,g6,g7,g8])
db.session.commit()