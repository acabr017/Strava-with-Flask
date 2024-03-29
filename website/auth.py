from sqlite3 import IntegrityError
import requests, os, datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from . import models, db
from sqlalchemy.sql import func

# from .models import User


auth = Blueprint("auth", __name__)


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
base_url = "https://www.strava.com/api/v3"
authorization_url = "https://www.strava.com/oauth/authorize"
token_url = "https://www.strava.com/api/v3/oauth/token"
redirect_uri = "http://127.0.0.1:5000/oauth_callback"
scope = "activity:read_all"


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


@auth.route("/login")
def strava():
    strava = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = strava.authorization_url(authorization_url)
    # return '<a href="' + login_url + '">Login with Strava</a>'
    return render_template("login.html", login_url=login_url)


@auth.route("/oauth_callback", methods=["GET"])
def oauth_callback():
    code = request.args.get("code")
    token_payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, params=token_payload)
    data = response.json()
    user = models.User.query.filter_by(strava_id=data["athlete"]["id"]).first()
    if not user:
        store_user_in_db(data)
        flash("User Added to Database")
    else:
        flash("User was already in Database")
    # print(user.id)
    get_athlete_activites(data["access_token"])
    return redirect("/")


def store_user_in_db(
    strava_user_info: dict,
):
    athlete_record = models.User(
        strava_id=strava_user_info["athlete"]["id"],
        firstname=strava_user_info["athlete"]["firstname"],
        lastname=strava_user_info["athlete"]["lastname"],
        access_token=strava_user_info["access_token"],
        refresh_token=strava_user_info["refresh_token"],
        expires_at=strava_user_info["expires_at"],
        expires_in=strava_user_info["expires_in"],
    )

    db.session.add(athlete_record)
    db.session.commit()

    return "User added to database"


def get_athlete_activites(access_token, per_page=200, page=1):
    # We have to give a header with our access token
    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {"Authorization": "Bearer " + access_token}
    param = {"per_page": 200, "page": 1}
    dataset = requests.get(activities_url, headers=header, params=param).json()
    print(type(dataset[0]["start_date_local"]))
    print(dataset[0]["start_date_local"][:10])
    for activity in dataset:
        date = datetime.datetime.strptime(activity["start_date_local"][:10], "%Y-%m-%d")
        if activity["type"] == "Run" and date >= datetime.datetime(2023, 1, 1):
            activity_record = models.Run(
                id=activity["id"],
                start_date=date,
                distance=activity["distance"],
                moving_time=activity["moving_time"],
                total_elevation_gain=activity["total_elevation_gain"],
                average_speed=activity["average_speed"],
                max_speed=activity["max_speed"],
                average_heartrate=activity["average_heartrate"],
                max_heartrate=activity["max_heartrate"],
                average_cadence=activity["average_cadence"],
                average_temp=activity["average_temp"],
                map_id=activity["map"]["id"],
                map_polyline=activity["map"]["summary_polyline"],
                owner_id=models.User.query.filter_by(
                    strava_id=activity["athlete"]["id"]
                )
                .first()
                .id,
            )
            db.session.add(activity_record)
            db.session.commit()


def get_total_activities(userID: str):
    totalActivities = models.Run.query.filter_by(owner_id=userID).count()
    return totalActivities


def get_total_distance(userID: str):
    totalDistance = (
        db.session.query(func.sum(models.Run.distance))
        .filter_by(owner_id=userID)
        .first()
    )
    return totalDistance


def get_total_time(userID: str):
    totalTime = (
        db.session.query(func.sum(models.Run.moving_time))
        .filter_by(owner_id=userID)
        .first()
    )
    time_as_int = int(totalTime[0])
    days = time_as_int // 86400
    hours = (time_as_int // 3600) % 24
    minutes = (time_as_int // 60) % 60
    seconds = time_as_int % 60
    time_output = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    return time_output


def get_average_speed(userID: str):
    # average_speed = (db.session.query(func.avg(models.Run.average_speed)).filter_by(owner_id=userID)
    pass
