from db.db import db
from models.task_model import Task


# ------------------ GET ALL TASKS ------------------

def get_all_tasks():
    tasks = Task.query.all()
    return [
        {
            "id": task.id,
            "title": task.title,
            "is_completed": task.is_completed
        }
        for task in tasks
    ]


# ------------------ CREATE TASK ------------------

def create_task(title):
    new_task = Task(title=title)

    db.session.add(new_task)
    db.session.commit()

    return {
        "id": new_task.id,
        "title": new_task.title,
        "is_completed": new_task.is_completed
    }


# ------------------ TOGGLE TASK ------------------

def toggle_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        raise ValueError("Task not found")

    task.is_completed = not task.is_completed
    db.session.commit()

    return {
        "id": task.id,
        "title": task.title,
        "is_completed": task.is_completed
    }


# ------------------ DELETE TASK ------------------

def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        raise ValueError("Task not found")

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted successfully"}