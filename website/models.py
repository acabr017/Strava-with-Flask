from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.Integer, unique=True, sqlite_on_conflict_unique="IGNORE")
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    access_token = db.Column(db.Integer)
    refresh_token = db.Column(db.String)
    expires_at = db.Column(db.Integer)
    expires_in = db.Column(db.Integer)
    token_created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    runs = db.relationship("Run")


class Run(db.Model):
    __tablename__ = "runs"

    run_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(
        db.Integer, nullable=False, unique=True, sqlite_on_conflict_unique="IGNORE"
    )
    start_date = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.REAL, nullable=False)
    moving_time = db.Column(db.REAL, nullable=False)
    total_elevation_gain = db.Column(db.REAL)
    average_speed = db.Column(db.REAL, nullable=False)
    max_speed = db.Column(db.REAL)
    average_heartrate = db.Column(db.Integer)
    max_heartrate = db.Column(db.Integer)
    average_cadence = db.Column(db.Integer)
    average_temp = db.Column(db.REAL)
    map_id = db.Column(db.String)
    map_polyline = db.Column(db.String)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


# class TotalRun(db.Model):
#     __tablename__ = "total_runs"

#     id = db.Column(db.Integer, primary_key=True)
#     owner_id = db.Column(
#         db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     total_distance = db.Column(db.REAL, nullable=False)
#     total_time = db.Column(db.REAL, nullable=False)


# class Token(db.Model):

#     __tablename__ = "tokens"

#     id = db.Column(db.Integer, primary_key=True)
#     user = db.relationship(User)
#     access_token = db.Column(db.Integer)
#     refresh_token = db.Column(db.String)
#     expires_at = db.Column(db.Integer)
#     expires_in = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id))
