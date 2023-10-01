from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Tarea(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

tareas_db = []

@app.post("/tasks/", response_model=Tarea)
async def create_task(task: Tarea):
    new_task = task.dict()
    tareas_db.append(new_task)
    return new_task

@app.get("/tasks/", response_model=List[Tarea])
async def get_tasks():
    if len(tareas_db)>0:
        return tareas_db
    raise HTTPException(status_code=200, detail="Aun no hay tareas pendientes")

@app.get("/tasks/{task_id}", response_model=Tarea)
async def get_task(task_id: int):
    if task_id < 0 or task_id >= len(tareas_db):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tareas_db[task_id]

@app.put("/tasks/{task_id}", response_model=Tarea)
async def update_task(task_id: int, task: Tarea):
    if task_id < 0 or task_id >= len(tareas_db):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    task_data = task.dict()
    tareas_db[task_id].update(task_data)
    return tareas_db[task_id]

@app.delete("/tasks/{task_id}", response_model=Tarea)
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tareas_db):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    deleted_task = tareas_db.pop(task_id)
    return deleted_task
