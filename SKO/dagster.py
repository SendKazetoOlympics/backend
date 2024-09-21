from dagster_graphql import DagsterGraphQLClient
from flask import Blueprint, request, jsonify, current_app

dagster_service = Blueprint("dagster", __name__)

def connect_dagster() -> DagsterGraphQLClient:
    return DagsterGraphQLClient("localhost", port_number=3000)

@dagster_service.route("/train_yolo_model", methods=["GET"])
def train_yolo_model():
    client = connect_dagster()
    client.submit_job_execution("train_yolo_model_job")