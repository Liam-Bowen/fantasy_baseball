import json

from dataclasses import dataclass
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from constants import *
import json
import csv

app = Flask(__name__)
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://fantasy_baseball:password@localhost/fantasy_baseball'
Session(app)


USER_KEY = 'user'
db = SQLAlchemy()
db.init_app(app)


@dataclass
class Player(db.Model):
    id: str
    name: str
    team: str
    league: str
    games: int
    at_bats: int
    runs: int
    hits: int
    doubles: int
    triples: int
    home_runs: int
    rbis: int
    stolen: int
    caught: int
    walks: int
    strikeout: int
    hbp: int
    sf: int
    ibb: int
    available: bool

    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    team = db.Column(db.String(256))
    league = db.Column(db.String(256))
    games = db.Column(db.Integer)
    at_bats = db.Column(db.Integer)
    runs = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    home_runs = db.Column(db.Integer)
    rbis = db.Column(db.Integer)
    stolen = db.Column(db.Integer)
    caught = db.Column(db.Integer)
    walks = db.Column(db.Integer)
    strikeout = db.Column(db.Integer)
    hbp = db.Column(db.Integer)
    sf = db.Column(db.Integer)
    ibb = db.Column(db.Integer)
    available = db.Column(db.Boolean, nullable=False, default=True)


with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        redirectTo = request.args.get('redirectTo')
        if redirectTo is None or redirectTo == '':
            redirectTo = '/'
        return render_template('login.html', redirectTo=redirectTo)
    elif request.method == 'POST':
        user_nm = request.form.get('username')
        passwd = request.form.get('password')
        redirectTo = request.form.get('redirectTo')
        print(f"Login for {user_nm} with {passwd}, redirecting to {redirectTo}")
        if redirectTo is None or redirectTo == '':
            redirectTo = '/'
        session[USER_KEY] = user_nm
        return redirect(redirectTo)


@app.route('/')
@app.route('/home', methods=['GET'])
def showHome():
    if USER_KEY in session:
        user = session[USER_KEY]
        return render_template('home.html', user=user)
    else:
        # show login
        return redirect(url_for('login', redirectTo='/'))


@app.route('/standings')
def standings():
    return render_template('standings.html')


@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html')


@app.route('/add-players')
def add_players():
    return render_template('add_players.html')


@app.route('/draft-room')
def draft_room():
    return render_template('draft_room.html')


@app.route('/api/players')
def get_all_players():
    if request.method == 'GET':
        queryResult = Player.query.filter_by(available=False).all()
        playerList = []
        for player in queryResult:
            playerList.append(player)
        return jsonify(playerList)


@app.route('/my-team')
def my_team2():
    return render_template('my_team.html')


#@app.route('/test')
#def test():
    #return render_template('test.html')


@app.route('/points-breakdown')
def points():

    return render_template('points.html')

app.run(debug=True)


if __name__ == '--main__':
    app.run()
