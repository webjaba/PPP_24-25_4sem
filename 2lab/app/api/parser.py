from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.schemas.tasks import TaskCreate, TaskOut
from app.models.models import TaskStatus
from app.services.auth.user import get_current_user
from app.cruds import tasks as task_crud
from app.services.parser import generate_graphml


router = APIRouter()


@router.post("/parse/", response_model=TaskOut)
async def start_parsing(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    task = task_crud.create_task(task_data.url, current_user.get("id"))

    async def run_parser():
        try:
            result = await generate_graphml(str(task_data.url), task_data.max_depth)
            task_crud.update_task_status(
                task.id, TaskStatus.completed, result=result
            )
        except Exception as e:
            print(e)
            task_crud.update_task_status(task.id, TaskStatus.failed)

    background_tasks.add_task(run_parser)
    return task


@router.get("/tasks/{task_id}/", response_model=TaskOut)
def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = task_crud.get_task_by_id(task_id, current_user.get("id"))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
