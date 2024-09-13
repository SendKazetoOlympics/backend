from flask import Blueprint, request, jsonify, current_app
from .database import connect_postgres
import uuid

webhook_service = Blueprint("webhook", __name__)

@webhook_service.route("/annotate_image", methods=["POST"])
def handle_annotate_image():
    print("Received POST request")
    if request.method == "POST":
        data = request.json
        frame_id = data["task"]["data"]["file_name"]
        client = connect_postgres()
        with client.cursor() as cursor:
            for annotation in data["annotation"]["result"]:
                if annotation["type"] == "rectanglelabels":
                    cursor.execute(
                        "INSERT INTO frame_rectangle_annotation (id, frame_id, class, x, y, width, height) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            uuid.uuid4(),
                            frame_id,
                            annotation["value"]["rectanglelabels"][0],
                            annotation["value"]["x"],
                            annotation["value"]["y"],
                            annotation["value"]["width"],
                            annotation["value"]["height"],
                        ),
                    )
                elif annotation["type"] == "choices":
                    cursor.execute(
                        "INSERT INTO frame_classification (id, frame_id, class) VALUES (%s, %s, %s)",
                        (
                            uuid.uuid4(),
                            frame_id,
                            annotation["value"]["choices"][0],
                        ),
                    )
                elif annotation["type"] == "keypointlabels":
                    cursor.execute(
                        "INSERT INTO frame_keypoint_annotation (id, frame_id, class, x, y) VALUES (%s, %s, %s, %s, %s)",
                        (
                            uuid.uuid4(),
                            frame_id,
                            annotation["value"]["keypointlabels"][0],
                            annotation["value"]["x"],
                            annotation["value"]["y"],
                        ),
                    )
            # Deduplicate the data
            cursor.execute(
                "DELETE FROM frame_rectangle_annotation a USING frame_rectangle_annotation b WHERE a.id < b.id AND a.frame_id = b.frame_id AND a.class = b.class AND a.x = b.x AND a.y = b.y AND a.width = b.width AND a.height = b.height"
            )
            cursor.execute(
                "DELETE FROM frame_classification a USING frame_classification b WHERE a.id < b.id AND a.frame_id = b.frame_id AND a.class = b.class"
            )
            cursor.execute(
                "DELETE FROM frame_keypoint_annotation a USING frame_keypoint_annotation b WHERE a.id < b.id AND a.frame_id = b.frame_id AND a.class = b.class AND a.x = b.x AND a.y = b.y"
            )
            client.commit()

        return jsonify({"message": "Success"})


@webhook_service.route("/test", methods=["POST"])
def test():
    print("Received POST request")
    if request.method == "POST":
        data = request.json
        print(data)
        return jsonify({"message": "Success"})
