import json

from dataclasses import dataclass
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from constants import *
import json
import csv

app = Flask(__name__)
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://fantasy_baseball:password@localhost/fantasy_baseball'
Session(app)

USER_KEY = 'userid'
__db__ = SQLAlchemy()
__db__.init_app(app)
Column = __db__.Column


@dataclass
class Batters(__db__.Model):
    id: str
    name: str
    tm: str
    lg: str
    g: int
    ab: int
    r: int
    h: int
    db: int
    tp: int
    hr: int
    rbi: int
    sb: int
    cs: int
    bb: int
    so: int
    hbp: int
    sf: int
    ibb: int
    roster_id: str

    id = __db__.Column(__db__.String(256), primary_key=True)
    name = __db__.Column(__db__.String(256))
    tm = __db__.Column(__db__.String(256))
    lg = __db__.Column(__db__.String(256))
    g = __db__.Column(__db__.Integer)
    ab = __db__.Column(__db__.Integer)
    r = __db__.Column(__db__.Integer)
    h = __db__.Column(__db__.Integer)
    db = __db__.Column(__db__.Integer)
    tp = __db__.Column(__db__.Integer)
    hr = __db__.Column(__db__.Integer)
    rbi = __db__.Column(__db__.Integer)
    sb = __db__.Column(__db__.Integer)
    cs = __db__.Column(__db__.Integer)
    bb = __db__.Column(__db__.Integer)
    so = __db__.Column(__db__.Integer)
    hbp = __db__.Column(__db__.Integer)
    sf = __db__.Column(__db__.Integer)
    ibb = __db__.Column(__db__.Integer)
    roster_id = __db__.Column(__db__.String, nullable=True, default=None)


@dataclass
class Pitchers(__db__.Model):
    id: str
    name: str
    tm: str
    lg: str
    w: int
    l: int
    g: int
    cg: int
    sho: int
    sv: int
    ip: float
    h: int
    er: int
    hr: int
    bb: int
    ibb: int
    so: int
    hbp: int
    available: bool

    id = __db__.Column(__db__.String(256), primary_key=True)
    name = __db__.Column(__db__.String(256))
    tm = __db__.Column(__db__.String(256))
    lg = __db__.Column(__db__.String(256))
    w = __db__.Column(__db__.Integer)
    l = __db__.Column(__db__.Integer)
    g = __db__.Column(__db__.Integer)
    cg = __db__.Column(__db__.Integer)
    sho = __db__.Column(__db__.Integer)
    sv = __db__.Column(__db__.Integer)
    ip = __db__.Column(__db__.Float)
    h = __db__.Column(__db__.Integer)
    er = __db__.Column(__db__.Integer)
    hr = __db__.Column(__db__.Integer)
    bb = __db__.Column(__db__.Integer)
    ibb = __db__.Column(__db__.Integer)
    so = __db__.Column(__db__.Integer)
    hbp = __db__.Column(__db__.Integer)
    available = __db__.Column(__db__.Boolean, nullable=False, default=True)


with app.app_context():
    __db__.create_all()


@app.route('/login', methods=['GET', 'POST'])
def show_handle_login():
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

@app.route('/logout', methods=['POST'])
def handle_logout():
    session.pop(USER_KEY)
    return redirect('/');


@app.route('/')
@app.route('/home', methods=['GET'])
def showHome():
    if USER_KEY in session:
        user = session[USER_KEY]
        return render_template('home.html', user=user)
    else:
        # show login
        return redirect(url_for('show_handle_login', redirectTo='/home'))


@app.route('/standings')
def show_standings():
    return render_template('standings.html')


@app.route('/scoreboard')
def show_scoreboard():
    return render_template('scoreboard.html')


@app.route('/add-players')
def show_handle_add_players():
    return render_template('add_players.html')


@app.route('/draft-room')
def show_draft_room():
    if request.method == 'GET':
        if USER_KEY in session:
            user_id = session[USER_KEY]
            return render_template('draft_room.html', user_id=user_id)
        else:
            return redirect(url_for('show_handle_login', redirectTo='/draft-room'))


@app.route('/api/batters')
def get_available_batters():
    if request.method == 'GET':
        if USER_KEY in session:
            user = session[USER_KEY]
            queryResult = Batters.query.filter_by(roster_id=None).all()
            playerList = []
            for player in queryResult:
                playerList.append(player)
            return jsonify(playerList)
        else:
            abort(401)


@app.route('/api/pitchers')
def get_all_pitchers():
    if request.method == 'GET':
        if USER_KEY in session:
            user = session[USER_KEY]
            queryResult = Pitchers.query.filter_by(available=True).all()
            pitcherList = []
            for pitcher in queryResult:
                pitcherList.append(pitcher)
            return jsonify(pitcherList)
        else:
            abort(401)


@app.route('/add_player', methods=['PUT'])
def add_player():
    if request.method == 'PUT':
        if USER_KEY in session:
            user = session[USER_KEY]
            json = request.json
            player_id = json['player-id']
            print(f"user {user} request to add player id {player_id}")
            player = Batters.query.get(player_id)
            if player is not None:
                print("Player is found")
                player.roster_id = user
                __db__.session.commit()
                print("Player roster change is committed")
                return '{"success": true}'
            return '{}'
        else:
            abort(401)
    else:
        abort(400)


@app.route('/my-team')
def my_team2():
    return render_template('my_team.html')


# @app.route('/test')
# def test():
# return render_template('test.html')


@app.route('/points-breakdown')
def points():
    return render_template('points.html')


app.run(debug=True)

if __name__ == '--main__':
    app.run()
