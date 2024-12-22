from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, select, update
from sqlmodel import Session

from app.models import Task, User
from app.schemas import CreateTaskSchema, UpdateTaskSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task_by_id(self, task_id: int) -> Task | None:
        task = self.db_session.get(Task, task_id)
        return task

    def get_tasks_by_date(self, selected_date: date, current_user: User) -> list[Task]:
        statement = (
            select(Task)
            .where(
                and_(Task.posted_at == selected_date, Task.user_id == current_user.id)
            )
            .order_by(Task.priority.asc())
        )
        result = self.db_session.exec(statement)
        tasks = result.scalars().all()
        return tasks

    def create_task(
        self, create_task_schema: CreateTaskSchema, current_user: User
    ) -> Task:
        task = Task(
            priority=create_task_schema.priority,
            text=create_task_schema.text,
            user_id=current_user.id,
            posted_at=create_task_schema.posted_at,
        )

        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def delete_task(self, task_id: int, user_id: int) -> bool:
        result = self.db_session.exec(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        task = result.scalar_one_or_none()
        if not task:
            return False

        self.db_session.delete(task)
        self.db_session.commit()
        return True

    def update_task(self, task: Task, new_task: UpdateTaskSchema) -> Task:
        if new_task.text:
            task.text = new_task.text
        if new_task.priority:
            task.priority = new_task.priority
        if new_task.completed is not None:
            task.completed = new_task.completed

        self.db_session.commit()
        self.db_session.refresh(task)

        return task

    def bulk_update_priorities(self, priorities: dict[int, int], current_user: User):
        """
        priorities hold id:new_priority key-pair dictionary
        """
        # make sure all tasks (ids) belong to the current user
        result = self.db_session.exec(
            select(Task.id).where(
                and_(Task.user_id == current_user.id, Task.id.in_(priorities))
            ),
        )
        task_ids = result.scalars().all()  # returns list of ids

        # task ids provided doesn't match task ids found for user
        if not len(priorities) == len(task_ids):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Provided ids doesn't match tasks of the user [{priorities}]",
            )

        # unpack into {id: key, priority:value} list
        priorities_to_update = [
            {"id": task_id, "priority": priority}
            for task_id, priority in priorities.items()
        ]

        self.db_session.exec(update(Task), priorities_to_update)
        self.db_session.commit()
