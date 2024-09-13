from flask import Blueprint, request, jsonify, current_app
import psycopg

database_service = Blueprint("database", __name__)

def connect_postgres() -> psycopg:
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"],
    )
    return database_client

@database_service.route("/insert_video", methods=["POST"])
def insert_video():
    pass

@database_service.route("/select_video_by_date", methods=["GET"])
def select_video_by_date():
    pass

@database_service.route("/select_video_by_type", methods=["GET"])
def select_video_by_type():
    pass

@database_service.route("/select_video_by_name", methods=["GET"])
def select_video_by_name():
    pass
