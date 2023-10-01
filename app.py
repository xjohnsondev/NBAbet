import os
import pdb
import datetime
from flask import Flask, jsonify, json, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy


import requests
from models import db, connect_db, User, Game, Ticket, Sportsbook
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



CURR_USER = "curr_user"
API_BASE_URL = "https://api.the-odds-api.com"
KEY = "7928e461c07e63ecb89b830c13c88065"

# DATE_FORMAT = '%b-%d '

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])

    else:
        g.user = None

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

        # new_game.game_date = datetime.datetime.strptime(game['commence_time'], DATE_FORMAT)



        db.session.add(new_game)
        db.session.commit()
    all_games = Game.query.all()
    return all_games

def refresh_games():
    table_delete = Game.games
    table_delete.drop()
    table_delete.create()
    return redirect('/action')

# @app.route('/get-data', methods=['GET'])
# def get_data():
#     data = Game.query.all()
#     return jsonify(data=all_games)

##############################################################################

@app.route('/')
def home_page():
    """Go to homepage"""
    # pdb.set_trace()
    return render_template('home.html')


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
# Betting routes

@app.route('/action')
def see_action():
    """See bet table"""

    if not g.user:
        flash("You must login to access this feature", 'danger')
        return redirect('/')
    else:
        # if gateway == 1:
        #     gateway = 0
            # get_new_data()

        all_games = Game.query.all()
        
        # pdb.set_trace()
        return render_template('action.html', all_games=all_games)

@app.route('/parlay-preview', methods=['GET','POST'])
def preview():
    if request.method == 'POST':
        # Get the JSON data from the ajax request
        data = request.get_json()
        print(data)
    return render_template('preview.html', data=data)