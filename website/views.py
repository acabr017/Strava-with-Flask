from flask import Blueprint, render_template
from flask_login import login_required
from .auth import get_total_activities, get_total_distance, get_total_time

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/leaderboard")
def leaderboard():

    total_activities = get_total_activities(1)
    total_distance_raw = get_total_distance(1)
    total_distance_miles = round((total_distance_raw[0] / 1609), 2)
    total_distance_km = round((total_distance_raw[0] / 1000), 2)
    total_time = get_total_time(1)

    return render_template(
        "leaderboard.html",
        total_runs=total_activities,
        total_distance_miles=total_distance_miles,
        total_distance_km=total_distance_km,
        total_time=total_time,
    )
