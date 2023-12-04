from main import app
from database import get_db
from database import ToDo
from settings.utils import get_serializers

from sqlalchemy.orm import Session
from fastapi import Request, Depends, Form
from fastapi.responses import JSONResponse


@app.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    todos = db_session.query(ToDo).all()
    return JSONResponse(content={"todos": get_serializers(todos)})


@app.post('/add')
def add(title: str = Form(...), db_session: Session = Depends(get_db)):
    new_todo = ToDo(title=title)
    db_session.add(new_todo)
    db_session.commit()
    return JSONResponse(content={"message": "Todo added successfully"})


@app.get('/update/{todo_id}')
def update(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter(ToDo.id == todo_id).first()
    todo.is_complete = not todo.is_complete
    db_session.commit()

    return JSONResponse(content={"message": "Todo updated successfully"})


@app.get('/delete/{todo_id}')
def delete(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter_by(id=todo_id).first()
    db_session.delete(todo)
    db_session.commit()

    return JSONResponse(content={"message": "Todo deleted successfully"})
