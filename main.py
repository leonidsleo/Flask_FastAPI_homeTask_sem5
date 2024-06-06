"""Задание

Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic."""

from fastapi import FastAPI, HTTPException
from pydantic import Field, BaseModel
from typing import Optional
import logging
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str = Field(max_length=100)
    description: Optional[str] = None
    status: str = 'не выполнено'


tasks = []


@app.get('/task/', response_model=list[Task])
async def get_task():
    return [task for task in tasks]


@app.post('/task/', response_model=Task)
async def post_task(task: Task):
    if [t for t in tasks if t.id == t.id]:
        raise HTTPException(status_code=409, detail='такая задача сущетвует')
    tasks.append(task)
    return task


@app.get('/task/{id}', response_model=Task)
async def get_id_task(id: int):
    task = [task for task in tasks if task.id == id]
    if not task:
        raise HTTPException(status_code=404, detail='нет задачи')
    return task[0]


@app.put('/task/', response_model=Task)
async def update_task(task: Task):
    for t in range(len(tasks)):
        if tasks[t].id == task.id:
            tasks[t] = task
            return tasks[t]
    raise HTTPException(status_code=404, detail='Такой задачи не существует')


@app.delete('/task/')
async def delete_task(id: int):
    for i in range(len(tasks)):
        if tasks[i].id == id:
            tasks.pop(i)
            return {'message': 'Задача удалена'}
    raise HTTPException(status_code=404, detail='Такой задачи нет')

