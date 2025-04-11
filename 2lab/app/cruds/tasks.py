from app.models.models import Task, TaskStatus
from app.db.session import SessionLocal


db = SessionLocal()


def create_task(url: str, user_id: int):
    task = Task(url=str(url), status=TaskStatus.pending, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(task_id: int, user_id: int):
    return (
        db
        .query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id)
        .first()
    )


def update_task_status(task_id: int, status: TaskStatus, result: str = None):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        if result:
            task.result = result
        db.commit()
        db.refresh(task)
    return task
