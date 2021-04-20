from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .dependancies import get_db
from .users import schemas, crud

app = FastAPI()


@app.get("/")
def read_root():
    return " sdfWodsfd"


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
