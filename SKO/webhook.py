from flask import Blueprint, request, jsonify, current_app

webhook_service = Blueprint("webhook", __name__)

@webhook_service.route("/annotate_image", methods=["POST"])
def handle_annotate_image():
    print("Received POST request")
    # if request.method == "POST":
    #     data = request.json
    #     print(data)
    #     for annotation in data["annotations"]['result']:
    #         if annotation['type'] == 'rectanglelabels':
    #             print(f"Label: {annotation['value']}")
    #             print(f"Coordinates: {annotation['rectanglelabels'][0]['rectangle']}")
    #         elif annotation['type'] == 'choices':
    #             print(f"Label: {annotation['value']}")
    #         elif annotation['type'] == 'keypointlabels':
    #             print(f"Label: {annotation['value']}")
    #             print(f"Coordinates: {annotation['keypointlabels'][0]['keypoint']}")

    #     return jsonify({"message": "Success"})
    return jsonify({"message": "Success"})
    
@webhook_service.route("/test", methods=["POST"])
def test():
    print("Received POST request")
    if request.method == "POST":
        data = request.json
        print(data)
        return jsonify({"message": "Success"})