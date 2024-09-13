from flask import Blueprint, request, jsonify, current_app
from label_studio_sdk.client import LabelStudio

labelstudio_service = Blueprint("labelstudio", __name__)

def connect_label_studio() -> LabelStudio:
    label_studio_client = LabelStudio(
        base_url=current_app.config["LABEL_STUDIO_URL"],
        api_key=current_app.config["LABEL_STUDIO_API_KEY"],
    )
    return label_studio_client

@labelstudio_service.route("/create_video_task", methods=["POST"])
def create_video_task():
    label_studio = connect_label_studio()
    data = request.get_json()
    task = label_studio.tasks.create(
        project_id = data["project_id"],
        data={
            "video_url": data["video_url"],
            "file_name": data["file_name"]
        }
    )
    return jsonify({"task": task})

