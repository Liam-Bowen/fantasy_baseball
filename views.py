from flask import Flask, render_template, session, redirect, url_for, request
from constants import *
from main import app


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


@app.route('/draft-room', methods=['GET', 'POST'])
def draft_room():
    if request.method == 'GET':
        playerList = [
            {
                "id": "--", "name": "--", "team": "--", "league": "--", "games": 0,
                "at_bat": 0, "runs": 0, "hits": 0, "doubles": 0, "triples": 0, "HR": 0, "RBI": 0,
                "SB": 0, "CS": 0, "BB": 0, "SO": 0, "HBP": 0, "SF": 0, "IBB": 0
            }
        ]
        return render_template('draft_room.html', playerList=playerList)
    elif request.method == "POST":
        playerToAdd = request.form['addPlayer']
        print(f'adding player id={playerToAdd} to roster')


@app.route('/my-team')
def my_team2():
    return render_template('my_team.html')


#@app.route('/test')
#def test():
    #return render_template('test.html')


@app.route('/points-breakdown')
def points():
    return render_template('points.html')