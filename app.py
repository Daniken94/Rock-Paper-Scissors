from flask import Flask, render_template, request, redirect, url_for, session 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import math
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    credits = db.Column(db.Integer, default=10)
    date_created = db.Column(db.DateTime, default=datetime.now)
    # User can have many game in stats
    statistics = db.relationship("Stats", backref="dbuser")

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plays = db.Column(db.Integer, default=0)
    credits_before = db.Column(db.Integer, default=10)
    win = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    tie = db.Column(db.Integer)
    credits_after = db.Column(db.Integer, default=10)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


MOVES = {
    "r": "ROCK",
    "s": "SCISSORS",
    "p": "PAPER",
}

@app.route('/', methods = ['GET', "POST"])
def start():
    if request.method == 'POST':
        if request.form["credits"] == str(10):
            form = request.form
            username = str(form["username"])
            credits = int(form["credits"])
            start_game = User(username=username, credits=credits)
            db.session.add(start_game)
            db.session.flush()
            player_id = start_game.id
            db.session.commit()
            player_stats = Stats(plays = 0, win = 0, lost = 1, tie = 0, user_id = player_id)
            db.session.add(player_stats)
            db.session.commit()
            return redirect(url_for("game", id=player_id))
        if request.form["credits"] == str(0):
            return render_template("game_over.html")
    return render_template("start_game.html")


@app.route('/game/<id>', methods = ['GET', "POST"])
def game(id):
    player = User.query.filter_by(id=id).first()
    player_stats = Stats.query.filter_by(user_id=id).first()
    message = ""
    credits_top = player.credits
    username = player.username

    
    if request.method == 'POST':
        form = request.form
        user = str(form["guess"]).lower()
        computer = random.choice(['r', 'p', 's'])

        while credits_top > 3:
            if computer == user:
                
                player.credits = player.credits - 3
                db.session.flush()
                credits = player.credits
                db.session.commit()

                player_stats.plays = player_stats.plays + 1
                db.session.flush()
                player_stats_play = player_stats.plays

                player_stats = Stats(plays = player_stats_play, credits_before = credits_top, credits_after = credits, win = 0, lost = 0, tie = 1, user_id=id)
                db.session.add(player_stats)
                db.session.commit()

                user = MOVES.get(user)
                message = f'It is a tie. You and the computer have both chosen {user}.'
                return render_template("game.html", message=message, credits=credits, username=username)
            elif (user == 'r' and computer == 's') or (user == 's' and computer == 'p') or (user == 'p' and computer == 'r'):
                player.credits = player.credits - 3
                db.session.flush()
                credits = player.credits
                db.session.commit()

                player_stats.plays = player_stats.plays + 1
                db.session.flush()
                player_stats_play = player_stats.plays
                
                player_stats = Stats(plays = player_stats_play, credits_before = credits_top, credits_after = credits, win = 0, lost = 1, tie = 0, user_id=id)
                db.session.add(player_stats)
                db.session.commit()

                user = MOVES.get(user)
                computer = MOVES.get(computer)
                message = f'You chose {user} and the computer chose {computer}. You lost :('
                return render_template("game.html", message=message, credits=credits, username=username)
            else:
                player.credits = player.credits + 1
                db.session.flush()
                credits = player.credits
                db.session.commit()

                player_stats.plays = player_stats.plays + 1
                db.session.flush()
                player_stats_play = player_stats.plays

                player_stats = Stats(plays = player_stats_play, credits_before = credits_top, credits_after = credits, win = 1, lost = 0, tie = 0, user_id=id)
                db.session.commit()

                user = MOVES.get(user)
                computer = MOVES.get(computer)
                message = f"You chose {user} and the computer chose {computer}. You won!"
                return render_template("game.html", message=message, credits=credits, username=username)
        else:
            return redirect(url_for("game_over", id=id))
    
    return render_template("game.html", message=message, credits=credits_top, username=username)



@app.route('/game_over/<id>', methods = ['GET', "POST"])
def game_over(id):
    player = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        form = request.form
        # another_credits = int(form["credits"])
        player.credits = player.credits + 10
        db.session.commit()
        return redirect(url_for("game", id=id))
    return render_template("game_over.html")





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
