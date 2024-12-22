from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session

from app.auth import get_current_user
from app.database import get_session
from app.models import User
from app.repositories.task_repo import TaskRepository
from app.schemas import (
    CreateTaskSchema,
    DisplayTaskSchema,
    UpdateTaskPrioritiesSchema,
    UpdateTaskSchema,
)

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=DisplayTaskSchema)
def add_task(
    create_task_schema: CreateTaskSchema,
    db_session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    task = task_repo.create_task(create_task_schema, current_user)
    return task


@router.get("/", response_model=list[DisplayTaskSchema])
def get_tasks(
    selected_date: date,
    db_session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    tasks = task_repo.get_tasks_by_date(selected_date, current_user)
    return tasks


@router.patch("/update-order/")
def update_tasks_order(
    priorities_schema: UpdateTaskPrioritiesSchema,
    db_session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)

    task_repo.bulk_update_priorities(priorities_schema.priorities, current_user)

    return "Priorities have been updated"


@router.patch("/{task_id}/", response_model=DisplayTaskSchema)
def update_task(
    task_id: int,
    update_task_schema: UpdateTaskSchema,
    db_session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    task = task_repo.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    if not task.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task does not belong to the current user",
        )

    updated_task = task_repo.update_task(task, new_task=update_task_schema)

    return updated_task


@router.delete("/{task_id}/")
def delete_task_by_id(
    task_id: str,
    db_session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)

    if not task_repo.delete_task(task_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"task with id {task_id} not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
