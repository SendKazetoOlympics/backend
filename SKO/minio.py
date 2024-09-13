from minio import Minio
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

minio_service = Blueprint("minio", __name__)

def connect_minio() -> Minio:
    minio_client = Minio(
        endpoint=current_app.config["MINIO_ENDPOINT"],
        access_key=current_app.config["MINIO_ACCESS_KEY"],
        secret_key=current_app.config["MINIO_SECRET_KEY"],
        secure=False,
    )
    return minio_client

@minio_service.route("/list_bucket", methods=["GET"])
def list_bucket():
    minio = connect_minio()
    buckets = minio.list_buckets()
    return jsonify({"buckets": buckets})

@minio_service.route("/list_objects", methods=["POST"])
def list_objects():
    minio = connect_minio()
    data = request.get_json()
    objects = minio.list_objects(data["bucket"])
    return jsonify({"objects": objects})

@minio_service.route("/get_presigned_url", methods=["POST"])
def get_presigned_url():
    minio = connect_minio()
    data = request.get_json()
    url = minio.presigned_get_object(data["bucket"], data["object"])
    return jsonify({"url": url})

@minio_service.route("/upload_file", methods=["POST"])
def upload_file():
    minio = connect_minio()
    file = request.files.getlist("file")[0]
    date = datetime.fromtimestamp(int(request.form.getlist("lastModified")[0])/1000)
    size = len(file.stream.read())
    file.stream.seek(0)
    year = date.year
    month = date.month
    day = date.day
    name = 'raw_data/' + str(year) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2) + '/' + file.filename
    minio.put_object(
        current_app.config["MINIO_BUCKET"],
        name,
        data = file,
        length = size,
        content_type='video/mp4'
    )
    return jsonify({"message": "Success"})