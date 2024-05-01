import schemas
from fastapi import FastAPI, Body, Depends
import models

from database import Base, engine, sessionmaker, SessionLocal
from sqlalchemy.orm import Session

def get_session():
    session = SessionLocal()
    try:
        yield session

    finally:
        session.close()

Base.metadata.create_all(engine)

app = FastAPI()

fakeDatabase = {
    1: {'task': 'Buy groceries'},
    2: {'task': 'Learn FastAPI'},
    3: {'task': 'Learn Fast'},
}


@app.get("/")
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

#Option 1
# @app.post("/")
# def add_item(task: str):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {'task': task}
#     return fakeDatabase

#Option 2
@app.post("/")
def add_item(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

#Option 3
# @app.post("/")
# def add_item(body: Body()):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {'task': body['task']}
#     return fakeDatabase


@app.put("/{id}")
def update_item(item_id: int, item: schemas.Item, session: Session = Depends(get_session)):
    item_object = session.query(models.Item).get(item_id)
    item_object.task = item.task
    session.commit()
    return item_object

@app.delete("/{id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item_object = session.query(models.Item).get(item_id)
    session.delete(item_object)
    session.commit()
    session.close()
    return item_object