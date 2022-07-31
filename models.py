from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, date, time



db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    credits = db.Column(db.Integer, default = 10)
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


