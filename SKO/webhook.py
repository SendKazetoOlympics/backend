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
            client.commit()
            # # Deduplicate the data
            # cursor.execute(
            #     "DELETE FROM frame_rectangle_annotation WHERE id IN (SELECT id FROM frame_rectangle_annotation GROUP BY frame_id, class, x, y, width, height HAVING COUNT(*) > 1)"
            # )
            # cursor.execute(
            #     "DELETE FROM frame_classification WHERE id IN (SELECT id FROM frame_classification GROUP BY frame_id, class HAVING COUNT(*) > 1)"
            # )
            # cursor.execute(
            #     "DELETE FROM frame_keypoint_annotation WHERE id IN (SELECT id FROM frame_keypoint_annotation GROUP BY frame_id, type, x, y HAVING COUNT(*) > 1)"
            # )

        return jsonify({"message": "Success"})


@webhook_service.route("/test", methods=["POST"])
def test():
    print("Received POST request")
    if request.method == "POST":
        data = request.json
        print(data)
        return jsonify({"message": "Success"})
