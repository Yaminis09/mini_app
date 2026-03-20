from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import logging

from services.task_service import (
    get_all_tasks,
    create_task,
    toggle_task,
    delete_task
)
from schemas.task_schema import TaskCreate

logging.basicConfig(level=logging.INFO)

task_bp = Blueprint("tasks", __name__)

# ------------------ BASIC ROUTES ------------------

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks())

@task_bp.route("/tasks", methods=["POST"])
def add_task():
    try:
        data = TaskCreate(**request.json)
        task = create_task(data.title)
        logging.info("Task created")
        return jsonify(task), 201

    except ValidationError as e:
        logging.error("Validation failed")
        return jsonify({"error": e.errors()}), 400

@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        task = toggle_task(task_id)
        return jsonify(task)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    try:
        result = delete_task(task_id)
        return jsonify(result)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# ------------------ OBSERVABILITY ------------------

@task_bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

# ------------------ VERIFICATION ------------------

@task_bp.route("/self-check", methods=["GET"])
def self_check():
    try:
        logging.info("Running self-check...")

        task = create_task("Self test task")
        toggle_task(task["id"])
        delete_task(task["id"])

        return {
            "status": "pass",
            "checks": [
                "create_task",
                "toggle_task",
                "delete_task"
            ]
        }

    except Exception as e:
        logging.error("Self-check failed")
        return {"status": "fail", "error": str(e)}, 500