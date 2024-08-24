from flask import Blueprint, request, jsonify, current_app
from minio import Minio
from label_studio_sdk.client import LabelStudio
import psycopg
import ffmpeg
import uuid

def connect_database() -> psycopg:
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"]
    )
    return database_client

def connect_minio() -> Minio:
    minio_client = Minio(
        endpoint=current_app.config["MINIO_ENDPOINT"],
        access_key=current_app.config["MINIO_ACCESS_KEY"],
        secret_key=current_app.config["MINIO_SECRET_KEY"]
    )
    return minio_client

def connect_label_studio() -> LabelStudio:
    label_studio_client = LabelStudio(
        base_url=current_app.config["LABEL_STUDIO_URL"],
        api_key=current_app.config["LABEL_STUDIO_API_KEY"]
    )
    return label_studio_client

database_service = Blueprint("database", __name__)

@database_service.route("/test", methods=["GET"])
def test():
    db = connect_database()
    minio = connect_minio()
    label_studio = connect_label_studio()
    return jsonify({"message": "Success"})