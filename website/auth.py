from sqlite3 import IntegrityError
import requests
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from . import models, db
from .models import User

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


@auth.route("/strava")
def strava():
    strava = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = strava.authorization_url(authorization_url)
    # session["oauth_state"] = state
    print(f"Login url {login_url}")
    #
    return '<a href="' + login_url + '">Login with Strava</a>'


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

    if not models.User.query.filter_by(strava_id=data["athlete"]["id"]).first():
        store_user_in_db(data)
        store_tokens_in_db(data)

        return "User Added to Database"
    return "Already in database"


def store_user_in_db(
    strava_user_info: dict,
):
    athlete_record = models.User(
        strava_id=strava_user_info["athlete"]["id"],
        firstname=strava_user_info["athlete"]["firstname"],
        lastname=strava_user_info["athlete"]["lastname"],
    )

    db.session.add(athlete_record)
    db.session.commit()

    return "User added to database"


def store_tokens_in_db(strava_token_info: dict):
    user = models.User.query.filter_by(
        strava_id=strava_token_info["athlete"]["id"]
    ).first()
    tokens_record = models.Token(
        access_token=strava_token_info["access_token"],
        refresh_token=strava_token_info["refresh_token"],
        expires_at=strava_token_info["expires_at"],
        expires_in=strava_token_info["expires_in"],
        user_id=user.id,
    )
    db.session.add(tokens_record)
    db.session.commit()
