from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import math

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)




# @app.route('/', methods = ['GET', "POST"])
# def guess():
#     counter = 0
#     message = ""
#     if request.method == 'POST':
#         counter += 1
#         form = request.form
#         user_guess = int(form["guess"])
#         comp_num = random.randint(1, 10)

#         if comp_num == user_guess:
#             message = "Well done, you got it"
#             return render_template("game_over.html", message=message)
#         elif comp_num > user_guess:
#             message = "Too low"
#         else:
#             message = "Too high"
#             if counter == 3:
#                 message = "You failed"
#                 return render_template("game_over.html", message=message)
#     return render_template("game.html", message=message)



@app.route('/', methods = ['GET', "POST"])
def game():
    counter = 0
    message = ""
    if request.method == 'POST':
        counter += 1
        form = request.form
        user = str(form["guess"]).lower()
        computer = random.choice(['r', 'p', 's'])

        if computer == user:
            message = f'It is a tie. You and the computer have both chosen {user}.'
            return render_template("game.html", message=message)
        elif (user == 'r' and computer == 's') or (user == 's' and computer == 'p') or (user == 'p' and computer == 'r'):
            message = f'You chose {user} and the computer chose {computer}. You lost :('
            return render_template("game.html", message=message)
        else:
            message = f"You chose {user} and the computer chose {computer}. You won!"
            return render_template("game.html", message=message)
    return render_template("game.html", message=message)





# def play():
#     user = input("What's your choice? 'r' for rock, 'p' for paper, 's' for scissors\n")
#     user = user.lower()

#     computer = random.choice(['r', 'p', 's'])

#     if user == computer:
#         return (0, user, computer)

#     # r > s, s > p, p > r
#     if is_win(user, computer):
#         return (1, user, computer)

#     return (-1, user, computer)

# def is_win(player, opponent):
#     # return true is the player beats the opponent
#     # winning conditions: r > s, s > p, p > r
#     if (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponent == 'r'):
#         return True
#     return False



# def play_best_of(n):
#     # play against the computer until someone wins best of n games
#     # to win, you must win ceil(n/2) games (ie 2/3, 3/5, 4/7)
#     player_wins = 0
#     computer_wins = 0
#     wins_necessary = math.ceil(n/2)
#     while player_wins < wins_necessary and computer_wins < wins_necessary:
#         result, user, computer = play()
#         # tie
#         if result == 0:
#             print('It is a tie. You and the computer have both chosen {}. \n'.format(user))
#         # you win
#         elif result == 1:
#             player_wins += 1
#             return ('You chose {} and the computer chose {}. You won!\n'.format(user, computer))
#         else:
#             computer_wins += 1
#             return ('You chose {} and the computer chose {}. You lost :(\n'.format(user, computer))

#     if player_wins > computer_wins:
#         return ('You have won the best of {} games! What a champ :D'.format(n))
#     else:
#         return ('Unfortunately, the computer has won the best of {} games. Better luck next time!'.format(n))


if __name__ == '__main__':
    app.run(debug=True)

    # play_best_of(3)