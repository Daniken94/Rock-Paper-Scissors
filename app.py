from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Stats, User
from sqlalchemy import desc, create_engine
from datetime import datetime
import random

app = Flask(__name__)

# Config database

# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/rps_db"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Stats.metadata.create_all(engine)
User.metadata.create_all(engine)


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
    # user = User.query.filter_by(id=id).first()
    player = db.session.query(User).filter_by(id=id).first()
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
    player = db.session.query(User).filter_by(id=id).first()
    if request.method == "POST":
        if request.form["guess"] == "stats":
            return redirect(url_for("statistics", id=id))
        elif request.form["guess"] == "10":
            player.credits = player.credits + 10
            db.session.commit()
            return redirect(url_for("game", id=id))
    return render_template("game_over.html")


# app for display stats. Stats are sorted by datetime from newest to oldest
@app.route("/stats/<id>", methods=["GET", "POST"])
def statistics(id):
    player = User.query.filter_by(id=id).first()
    stats_all = Stats.query.filter_by(user_id=id).order_by(desc("datetime_created"))
    stats = Stats.query.filter(
        Stats.user_id == id, Stats.date_created == datetime.today().strftime("%Y-%m-%d")
    ).order_by(desc("datetime_created"))

    # for in loop to aggregate sum of win, lost, tie and plays.
    plays = []
    wins = []
    losts = []
    ties = []

    for play in stats:
        i = play.plays
        w = play.win
        l = play.lost
        t = play.tie
        plays.append(i)
        wins.append(w)
        losts.append(l)
        ties.append(t)
    plays = sum(plays)
    wins = sum(wins)
    losts = sum(losts)
    ties = sum(ties)

    # for in loop to aggregate sum of win, lost, tie and plays in all days from player ID.

    plays_all = []
    wins_all = []
    losts_all = []
    ties_all = []

    for play in stats_all:
        i = play.plays
        w = play.win
        l = play.lost
        t = play.tie
        plays_all.append(i)
        wins_all.append(w)
        losts_all.append(l)
        ties_all.append(t)
    plays_all = sum(plays_all)
    wins_all = sum(wins_all)
    losts_all = sum(losts_all)
    ties_all = sum(ties_all)

    if request.method == "POST":
        if request.form["guess"] == "old":
            return redirect(url_for("game", id=id))
        elif request.form["guess"] == "new":
            return redirect(url_for("start"))
    return render_template(
        "stats.html",
        stats=stats,
        stats_all=stats_all,
        player=player,
        plays=plays,
        wins=wins,
        losts=losts,
        ties=ties,
        plays_all=plays_all,
        wins_all=wins_all,
        losts_all=losts_all,
        ties_all=ties_all,
    )


if __name__ == "__main__":
    # Create database if not exist
    db.create_all()
    app.run(debug=True)
