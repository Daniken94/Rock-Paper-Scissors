from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, date
import random

app = Flask(__name__)

# Config database

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

# Database models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    credits = db.Column(db.Integer, default=10)
    datetime_created = db.Column(db.DateTime, default=datetime.now)
    date_created = db.Column(db.Date, default=date.today)
    # User can have many game in stats
    statistics = db.relationship("Stats", backref="dbuser")

    # validate username. Required field
    @validates("username")
    def validate_name(self, key, value):
        if value == "":
            raise ValueError("Please type your name")
        return value


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plays = db.Column(db.Integer, default=0)
    credits_before = db.Column(db.Integer, default=0)
    win = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    tie = db.Column(db.Integer)
    credits_after = db.Column(db.Integer, default=10)
    datetime_created = db.Column(db.DateTime, default=datetime.now)
    date_created = db.Column(db.Date, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Dict for form select answer

MOVES = {
    "r": "ROCK",
    "s": "SCISSORS",
    "p": "PAPER",
}

# App for start game


@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        if request.form["credits"] == str(10):
            form = request.form
            username = str(form["username"])
            credits = int(form["credits"])
            # Saving User and Stats in database
            start_game = User(username=username, credits=credits)
            db.session.add(start_game)
            db.session.flush()
            # flush it's importatn for catch player id
            player_id = start_game.id
            db.session.commit()
            player_stats = Stats(plays=0, win=0, lost=0, tie=0, user_id=player_id)
            db.session.add(player_stats)
            db.session.commit()
            return redirect(url_for("game", id=player_id))

    return render_template("start_game.html")


# Game. Need ID for colecting data in database
@app.route("/game/<id>", methods=["GET", "POST"])
def game(id):
    player = User.query.filter_by(id=id).first()
    player_stats = Stats.query.filter_by(user_id=id).first()
    message = ""
    credits_top = player.credits
    username = player.username
    # double IF for check POSt metchod and check request from server. After check app
    # continue play or go to statistics app.
    if request.method == "POST":
        if request.form["guess"] == "stats":
            return redirect(url_for("statistics", id=id))
        elif request.form["guess"] == "r" or "p" or "s":
            form = request.form
            user = str(form["guess"]).lower()
            computer = random.choice(["r", "p", "s"])
            while credits_top > 0:
                if computer == user:
                    # saving credits status in database
                    player.credits = player.credits - 3
                    db.session.flush()
                    credits = player.credits
                    db.session.commit()
                    # saving player stats in database
                    player_stats = Stats(
                        plays=1,
                        credits_before=credits_top,
                        credits_after=credits,
                        win=0,
                        lost=0,
                        tie=1,
                        user_id=id,
                    )
                    db.session.add(player_stats)
                    db.session.commit()
                    # use dict for user and computer request
                    user = MOVES.get(user)
                    message = (
                        f"It is a tie. You and the computer have both chosen {user}."
                    )
                    return render_template(
                        "game.html", message=message, credits=credits, username=username
                    )
                elif (
                    (user == "r" and computer == "s")
                    or (user == "s" and computer == "p")
                    or (user == "p" and computer == "r")
                ):
                    player.credits = player.credits - 3
                    db.session.flush()
                    credits = player.credits
                    db.session.commit()

                    player_stats = Stats(
                        plays=1,
                        credits_before=credits_top,
                        credits_after=credits,
                        win=0,
                        lost=1,
                        tie=0,
                        user_id=id,
                    )
                    db.session.add(player_stats)
                    db.session.commit()

                    user = MOVES.get(user)
                    computer = MOVES.get(computer)
                    message = f"You chose {user} and the computer chose {computer}. You lost :("
                    return render_template(
                        "game.html", message=message, credits=credits, username=username
                    )
                else:
                    player.credits = player.credits + 1
                    db.session.flush()
                    credits = player.credits
                    db.session.commit()

                    player_stats = Stats(
                        plays=1,
                        credits_before=credits_top,
                        credits_after=credits,
                        win=1,
                        lost=0,
                        tie=0,
                        user_id=id,
                    )
                    db.session.add(player_stats)
                    db.session.commit()

                    user = MOVES.get(user)
                    computer = MOVES.get(computer)
                    message = (
                        f"You chose {user} and the computer chose {computer}. You won!"
                    )
                    return render_template(
                        "game.html", message=message, credits=credits, username=username
                    )
            else:
                return redirect(url_for("game_over", id=id))
    return render_template(
        "game.html", message=message, credits=credits_top, username=username
    )


# app for game over template. If you have got less than 0 credits in
# game over template you can add next 10 credits
@app.route("/game_over/<id>", methods=["GET", "POST"])
def game_over(id):
    player = User.query.filter_by(id=id).first()
    if request.method == "POST":
        if request.form["guess"] == "stats":
            return redirect(url_for("statistics", id=id))
        elif request.form["guess"] == "10":
            player.credits = player.credits + 10
            db.session.commit()
            return redirect(url_for("game", id=id))
    return render_template("game_over.html")


# app for display stats
@app.route("/stats/<id>", methods=["GET", "POST"])
def statistics(id):
    player = User.query.filter_by(id=id).first()
    stats = Stats.query.filter_by(user_id=id)
    stats2 = Stats.query.filter(
        Stats.user_id == id, Stats.date_created == datetime.today().strftime("%Y-%m-%d")
    )

    # for in loop to aggregate sum of win, lost, tie and plays.
    plays = []
    wins = []
    losts = []
    ties = []

    for play in stats2:
        i = play.plays
        w = play.win
        l = play.lost
        t = play.tie
        plays.insert(0, i)
        wins.insert(0, w)
        losts.insert(0, l)
        ties.insert(0, t)
    plays = sum(plays)
    wins = sum(wins)
    losts = sum(losts)
    ties = sum(ties)

    if request.method == "POST":
        if request.form["guess"] == "old":
            return redirect(url_for("game", id=id))
        elif request.form["guess"] == "new":
            return redirect(url_for("start"))
    return render_template(
        "stats.html",
        stats=stats,
        player=player,
        plays=plays,
        wins=wins,
        losts=losts,
        ties=ties,
    )


if __name__ == "__main__":
    # Create database if not exist
    db.create_all()
    app.run(debug=True)
