from flask import Flask, request
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from src.helper.Helper import Helper
from datetime import timedelta
from dotenv import dotenv_values

app = Flask(__name__)

# connection to db
ENV_CONFIG = dotenv_values(".env")
ACCESS_EXPIRES= 30
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ENV_CONFIG['DATABASE_URL']

app.config.update({
    "TESTING": True,
    "TEMPLATES_AUTO_RELOAD":True
})

helper = Helper()

from src.routes.user_route import user_route
from src.routes.transaction_route import transaction_route
from src.routes.account_route import account_route

app.register_blueprint(user_route)
app.register_blueprint(account_route)
app.register_blueprint(transaction_route)


@app.route("/", methods =["GET"])
def hello_world():
    if request.method == "GET":
        location_ip = helper.reveal_location(request.remote_addr)
        return helper.response_message(result={
           "result":location_ip
        })
