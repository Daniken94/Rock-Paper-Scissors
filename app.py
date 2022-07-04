from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# import random


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)


@app.route('/<name>/<location>')
def index(name, location):
    user = Test(name=name, location=location)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added new user!<h1>'

@app.route('/<name>')
def get_user(name):
    user = Test.query.filter_by(name=name).first()

    return f"<h1>User is located in: {user.location}<h1>"






# class Game(Base):
#     __tablename__ = "game"

#     player_id = Column(Integer, primary_key=True)
#     username = Column(String)
#     player_credits = Column(Integer, default=10)
#     stats_win = Column(Integer)
#     stats_lose = Column(Integer)
#     created_date = Column(DateTime, default=datetime.datetime.utcnow)

#     def __init__(self, player_id, username, player_credits, stats_win, stats_lose, created_date):
#         self.player_id = player_id
#         self.username = username
#         self.player_credits - player_credits
#         self.stats_win = stats_win
#         self.stats_lose = stats_lose
#         self.created_date = created_date





# CHOICES = 'rps'


# def get_player_choice():
#     """Get user input and validate it is one of the choices above"""
#     player_choice = None
#     while player_choice is None:
#         player_choice = input('Choices: \n(R)ock \n(P)aper \n(S)cissors \n\nPick: ')
#         if player_choice.lower() not in CHOICES:
#             player_choice = None
#     return player_choice.lower()


# def get_computer_choice():
#     """Have the computer pick one of the valid choices at random"""
#     computer_choice = random.randint(0, 2)
#     computer_choice = CHOICES[computer_choice]
#     return computer_choice


# def is_draw(player_choice, computer_choice):
#     """Check if game was a draw"""
#     if player_choice == computer_choice:
#         return True


# def print_winner(player_choice, computer_choice):
#     """Check to see who won"""
#     if player_choice == 'r' and computer_choice == 's':
#         print('Player wins!')
#     elif player_choice == 's' and computer_choice == 'p':
#         print('Player wins!')
#     elif player_choice == 'p' and computer_choice == 'r':
#         print('Player wins!')
#     else:
#         print('Computer wins!')
#         print('%s beats %s' % (computer_choice, player_choice))


# def play_game():
#     """play the game"""
#     player_choice = get_player_choice()
#     computer_choice = get_computer_choice()
#     if is_draw(player_choice, computer_choice):
#         print("It's a draw, both players picked %s: " % player_choice)
#     else:
#         print("Computer picked: %s" % computer_choice)
#         print("Player picked: %s" % player_choice)
#         print_winner(player_choice, computer_choice)


# if __name__ == "__main__":
#     play_game()