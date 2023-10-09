import os
import pdb
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, json, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


import requests
from models import db, connect_db, User, Game, Ticket, Counter
from forms import LoginForm, RegisterForm

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///nbabet'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "keyz")
toolbar = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.create_all()

CURR_USER = "curr_user"
API_BASE_URL = "https://api.the-odds-api.com"
KEY = "7928e461c07e63ecb89b830c13c88065"

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])
        get_day()

    else:
        g.user = None
    
def get_day():
    """Retrieve current day"""
    session['today'] = datetime.now().strftime("%b %d")

def do_login(user):
    """Login user"""
    session[CURR_USER] = user.id

def do_logout():
    """Logout user"""

    if CURR_USER in session:
        del session[CURR_USER]

def get_new_data():
    res = requests.get(f"{API_BASE_URL}/v4/sports/basketball_nba/odds",
                           params={'apiKey': KEY, 
                                   'regions': 'us', 
                                   'markets': 'h2h,spreads,totals',
                                   'oddsFormat': 'american',
                                   'bookmakers': 'draftkings'})
    data = res.json()
    # pdb.set_trace()
    for game in data:
        new_game = Game()
        new_game.game_id = game['id']
        new_game.home_team = game['home_team']
        new_game.away_team = game['away_team']
        new_game.home_ml_price = game['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
        new_game.away_ml_price = game['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
        new_game.home_PS = game['bookmakers'][0]['markets'][1]['outcomes'][0]['point']
        new_game.away_PS = game['bookmakers'][0]['markets'][1]['outcomes'][1]['point']
        new_game.home_PS_price = game['bookmakers'][0]['markets'][1]['outcomes'][0]['price']
        new_game.away_PS_price = game['bookmakers'][0]['markets'][1]['outcomes'][1]['price']
            
        if 'markets' in game['bookmakers'][0] and len(game['bookmakers'][0]['markets']) > 2:
             new_game.over_under = game['bookmakers'][0]['markets'][2]['outcomes'][0]['point']
        else:
            new_game.over_under = 'OFF'

        if 'markets' in game['bookmakers'][0] and len(game['bookmakers'][0]['markets']) > 2:
            new_game.over_under_price = game['bookmakers'][0]['markets'][2]['outcomes'][0]['price']
        else:
            new_game.over_under_price = 0

        iso_time_string = game['commence_time']

        # Parse the ISO time string into a datetime object
        year = int(iso_time_string[0:4])
        month = int(iso_time_string[5:7])
        day = int(iso_time_string[8:10])
        hour = int(iso_time_string[11:13])
        minute = int(iso_time_string[14:16])

        iso_datetime = datetime(year, month, day, hour, minute)
        
        # Offset time to PST
        pst_datetime = iso_datetime-timedelta(hours=7)
        formatted_time = pst_datetime.strftime("%b %d, %Y @ %I:%M %p")
        new_game.start_time = formatted_time

        db.session.add(new_game)
        db.session.commit()
    all_games = Game.query.all()
    return all_games

def refresh_games():
    table_delete = Game.games
    table_delete.drop()
    table_delete.create()
    return redirect('/action')


##############################################################################
# User signup/login/logout

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Go to register/login page - handle registration/login"""
    login_form = LoginForm()
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        try:
            user = User.signup(
                username=register_form.username.data,
                password=register_form.password.data,
                email=register_form.email.data
            )
            if not Counter.query.get(1):
                start_counter = Counter()
                db.session.add(start_counter)
                db.session.commit()
            counter = Counter.query.get(1)
            counter.total_users += 1
            db.session.commit()
            do_login(user)
            return redirect('/')

        except IntegrityError:
            flash("Username already taken", 'danger')
        
    elif login_form.validate_on_submit():
        user = User.authenticate(login_form.username.data, login_form.password.data)
        if user:
            do_login(user)
            return redirect('/')

    return render_template('login.html', login_form=login_form, register_form=register_form)

@app.route('/logout')
def logout():
    """Log out of session"""
    session.pop(CURR_USER)
    return redirect('/')

##############################################################################

@app.route('/')
def home_page():
    """Go to homepage"""
    # pdb.set_trace()
    
    current_time = datetime.now().strftime("%b %d, %Y @ %I:%M %p")   
    print(current_time)

    # games = Game.query.filter_by(day = session['today']).all()
    # print(games[0].id)

    return render_template('home.html')

@app.route('/reset-balance', methods=["POST"])
def reset_balance():
    """Reset balance to $1000"""

    user = User.query.get(g.user.id)
    user.balance = float(request.data)
    db.session.commit()
    return redirect('/')


##############################################################################
# Betting routes


@app.route('/action')
def see_action():
    """See bet table"""

    if not g.user:
        flash("You must login to access this feature", 'danger')
        return redirect('/')
    else:
        # get_new_data()

        """Table resets at midnight PST daily"""
        # current_day = datetime.now().strftime("%b %d")  
        current_day = ("Oct 24")
        print(current_day)
        all_games = Game.query.filter_by(day = current_day).all()
        
        return render_template('action.html', all_games=all_games, g=g)

@app.route('/parlay-preview', methods=['GET','POST'])
def preview():
    if request.method == 'POST':
        # Get the JSON data from the ajax request
        data = request.get_json()
        print(data)
    return render_template('preview.html', data=data)

@app.route('/submit-parlay', methods=['POST', 'GET'])
def submit_parlay():
    """Submit selected parlay ticket"""
    print('############################################################')
    if request.method == 'POST':
        data=request.get_json()
        print(data)
        if not Counter.query.get(1):
            counter = Counter()
            db.session.add(counter)
            db.session.commit()

        counter = Counter.query.get(1)

        for pick in data["key1"]:
            new_ticket = Ticket()
            new_ticket.user_id = pick['user']
            new_ticket.game_id = pick['game_id']
            new_ticket.bet_id = counter.value
            new_ticket.pick = pick['parlayChoice1']
            new_ticket.points = pick['parlayChoice2']
            new_ticket.odds = pick['parlayChoice3']
            new_ticket.amount_bet = float(data["betAmount"])
            new_ticket.to_win = float(data["toWin"])
            
            # print(type(game['parlayChoice2']))

            db.session.add(new_ticket)
            db.session.commit()

        
        counter.value += 1
        counter.total_bets += 1
        user = User.query.get(g.user.id)
        user.balance -= float(data["betAmount"])
        db.session.commit()
        print(user.balance)
    return redirect('/')
    
@app.route('/parlays/<user>')
def show_parlays(user):
    """Show user parlays"""
    if user != g.user.username:
        flash("You do not have permissions to view that page", 'alert alert-danger')
        return redirect('/')
    g_user = User.query.filter_by(username = user).first()
    user_parlays = Ticket.query.filter_by(user_id = g_user.id).all()

    bet_list = [[parlay.bet_id, parlay.amount_bet, parlay.to_win] for parlay in user_parlays]
    bet_set = set(map(tuple, bet_list))

    # pdb.set_trace()
    return render_template('parlays.html', user_parlays=user_parlays, bet_list=bet_set)

@app.route('/parlays/details/<int:bet_id>')
def show_parlay(bet_id):
    """Show details of selected parlay"""

    bets = Ticket.query.filter_by(bet_id=bet_id).all()
    print(bets)
    # pdb.set_trace()
    return render_template('parlay.html', bets=bets)