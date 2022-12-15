import json

from dataclasses import dataclass
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from constants import *
import json

app = Flask(__name__)
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://fantasy_baseball:password@localhost/fantasy_baseball'
Session(app)

USER_KEY = 'userid'
TEAM_KEY = 'teamid'
__db__ = SQLAlchemy()
__db__.init_app(app)
Column = __db__.Column


@dataclass
class Users(__db__.Model):
    username: str
    password: str
    teamName: str

    username = __db__.Column(__db__.String(256), primary_key=True)
    password = __db__.Column(__db__.String(256))
    teamName = __db__.Column(__db__.String(256), unique=True)

    def __init__(self, username, password, teamName):
        self.username = username
        self.password = password
        self.teamName = teamName


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
    pos: str

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
    pos = __db__.Column(__db__.String(256))


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
    roster_id: str
    pos: str

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
    roster_id = __db__.Column(__db__.String(256), nullable=True, default=None)
    pos = __db__.Column(__db__.String(256))


with app.app_context():
    __db__.create_all()


@app.route('/login', methods=['GET', 'POST'])
def show_handle_login():
    if USER_KEY in session:
        session.pop(USER_KEY)
    if request.method == 'GET':
        redirectTo = request.args.get('redirectTo')
        if redirectTo is None or redirectTo == '':
            redirectTo = '/'
        return render_template('login.html', redirectTo=redirectTo)
    elif request.method == 'POST':
        user_nm = request.form.get('username')
        passwd = request.form.get('password')
        redirectTo = request.form.get('redirectTo')
        user = Users.query.get(user_nm)
        if user is not None:
            if passwd == user.password:
                print(f"Login for {user_nm} with {passwd}, redirecting to {redirectTo}")
                if redirectTo is None or redirectTo == '':
                    redirectTo = '/'
                session[USER_KEY] = user.username
                session[TEAM_KEY] = user.teamName
                return redirect(redirectTo)
        return render_template('login.html', redirectTo=redirectTo, msg="Invalid username or Password")


@app.route('/register', methods=['GET', 'POST'])
def show_handle_register():
    if USER_KEY in session:
        session.pop(USER_KEY)
    if request.method == 'GET':
        redirectTo = request.args.get('redirectTo')
        if redirectTo is None or redirectTo == '':
            redirectTo = '/'
        return render_template('register.html', redirectTo=redirectTo)
    if request.method == 'POST':
        user_nm = request.form.get('username')
        passwd = request.form.get('password')
        team_nm = request.form.get('teamName')
        redirectTo = request.form.get('redirectTo')
        try:
            new_user = Users(user_nm, passwd, team_nm)
            __db__.session.add(new_user)
            __db__.session.commit()
            session[USER_KEY] = new_user.username
            session[TEAM_KEY] = new_user.teamName
            return redirect(redirectTo)
        except:
            return render_template('register.html', redirectTo=redirectTo, msg="Enter a different username")


@app.route('/logout', methods=['POST'])
def handle_logout():
    session.pop(USER_KEY)
    return redirect('/');


@app.route('/')
@app.route('/home', methods=['GET'])
def showHome():
    if USER_KEY in session:
        user = session[USER_KEY]
        team = session[TEAM_KEY]
        return render_template('home.html', user=user)
    else:
        # show login
        return redirect(url_for('show_handle_login', redirectTo='/home'))


# @app.route('/standings')
# def show_standings():
    # return render_template('standings.html')


@app.route('/compare-teams')
def show_comparison():
    return render_template('comparison.html')


# @app.route('/add-players')
# def show_handle_add_players():
    # return render_template('add_players.html')


@app.route('/draft-room')
def show_draft_room():
    if request.method == 'GET':
        if USER_KEY in session:
            user_id = session[USER_KEY]
            team = session[TEAM_KEY]
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
            queryResult = Pitchers.query.filter_by(roster_id=None).all()
            pitcherList = []
            for pitcher in queryResult:
                pitcherList.append(pitcher)
            return jsonify(pitcherList)
        else:
            abort(401)


@app.route('/api/roster')
def get_player_roster():
    if request.method == 'GET':
        if USER_KEY in session:
            user = session[USER_KEY]
            team = session[TEAM_KEY]
            rosterList = []
            pitcherQueryResult = Pitchers.query.filter_by(roster_id=team).all()
            for pitcher in pitcherQueryResult:
                roster_entry = json.loads(jsonify(pitcher).data)
                roster_entry['position'] = 'pitcher'
                rosterList.append(roster_entry)
            batterQueryResult = Batters.query.filter_by(roster_id=team).all()
            for batter in batterQueryResult:
                roster_entry = json.loads(jsonify(batter).data)
                roster_entry['position'] = 'batter'
                rosterList.append(roster_entry)
            return jsonify(rosterList)
        else:
            abort(401)


@app.route('/api/roster/<team>')
def get_team_roster(team):
    if request.method == 'GET':
        if USER_KEY in session:
            rosterList = []
            pitcherQueryResult = Pitchers.query.filter_by(roster_id=team).all()
            for pitcher in pitcherQueryResult:
                roster_entry = json.loads(jsonify(pitcher).data)
                roster_entry['position'] = 'pitcher'
                rosterList.append(roster_entry)
            batterQueryResult = Batters.query.filter_by(roster_id=team).all()
            for batter in batterQueryResult:
                roster_entry = json.loads(jsonify(batter).data)
                roster_entry['position'] = 'batter'
                rosterList.append(roster_entry)
            return jsonify(rosterList)
        else:
            abort(401)


@app.route('/api/teams')
def get_teams():
    if request.method == 'GET':
        if USER_KEY in session:
            teamList = []
            userQueryResult = Users.query.all()
            for user in userQueryResult:
                user_entry = json.loads(jsonify(user).data)
                teamList.append(user_entry['teamName'])
            return jsonify(teamList)
        else:
            abort(401)


@app.route('/api/roster/batters/add', methods=['PUT'])
def add_batter_to_roster():
    if request.method == 'PUT':
        if USER_KEY in session:
            user = session[USER_KEY]
            team = session[TEAM_KEY]
            json = request.json
            batterCountQueryResult = Batters.query.filter_by(roster_id=team).count()
            if batterCountQueryResult < 10:
                player_id = json['player-id']
                print(f"user {user} request to add batter id {player_id}")
                player = Batters.query.get(player_id)
                if player is not None:
                    print("Player is found")
                    player.roster_id = team
                    __db__.session.commit()
                    print("Player roster change is committed")
                    return '{"success": true}'
                return f'{{"error": "no batter found for {player_id}"}}'
            else:
                return f'{{"error": "batter roster is full"}}'
        else:
            abort(401)
    else:
        abort(400)


@app.route('/api/roster/pitchers/add', methods=['PUT'])
def add_pitcher_to_roster():
    if request.method == 'PUT':
        if USER_KEY in session:
            user = session[USER_KEY]
            team = session[TEAM_KEY]
            json = request.json
            pitcherCountQueryResult = Pitchers.query.filter_by(roster_id=team).count()
            if pitcherCountQueryResult < 6:
                player_id = json['player-id']
                print(f"user {user} request to add pitcher id {player_id}")
                player = Pitchers.query.get(player_id)
                if player is not None:
                    print("Player is found")
                    player.roster_id = team
                    __db__.session.commit()
                    print("Player roster change is committed")
                    return '{"success": true}'
                return f'{{"error": "no pitcher found for {player_id}"}}'
            else:
                return f'{{"error": "pitcher roster is full"}}'
        else:
            abort(401)
    else:
        abort(400)


@app.route('/api/roster/batters/remove', methods=['DELETE'])
def remove_batter_from_roster():
    if request.method == 'DELETE':
        if USER_KEY in session:
            user = session[USER_KEY]
            team = session[TEAM_KEY]
            jsonBody = request.json
            player_id = jsonBody['player-id']
            print(f"user {user} request to remove batter id {player_id}")
            player = Batters.query.filter_by(roster_id=team).filter_by(id=player_id).one()
            if player is not None:
                player.roster_id = None
                __db__.session.commit()
                return '{"success": true}'
            return f'{{"error": "no batter found for {player_id}"}}'
        else:
            abort(401)
    else:
        abort(400)


@app.route('/api/roster/pitchers/remove', methods=['DELETE'])
def remove_pitchers_from_roster():
    if request.method == 'DELETE':
        if USER_KEY in session:
            user = session[USER_KEY]
            team = session[TEAM_KEY]
            jsonBody = request.json
            player_id = jsonBody['player-id']
            print(f"user {user} request to remove pitcher id {player_id}")
            player = Pitchers.query.filter_by(roster_id=team).filter_by(id=player_id).one()
            if player is not None:
                player.roster_id = None
                __db__.session.commit()
                return '{"success": true}'
            return f'{{"error": "no pitcher found for {player_id}"}}'
        else:
            abort(401)
    else:
        abort(400)


@app.route('/my-team')
def my_team2():
    return render_template('my_team.html')


@app.route('/points-breakdown')
def points():
    return render_template('points.html')


app.run(debug=True)

if __name__ == '--main__':
    app.run()
