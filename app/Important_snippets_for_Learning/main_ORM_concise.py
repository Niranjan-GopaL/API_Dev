from fastapi import FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import models, database

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
     title: str
     content: str
     is_published : bool = True

# COMPLETE LIST OF EVERYTHING ; CONCISE !!

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_to_delete = db.query(models.Post).filter(models.Post.id_sqlalc == id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post_to_update: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id_sqlalc == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post_query.update(post_to_update.dict())
    db.commit()
    return {"data updated!": post_query.first()}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id_sqlalc == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)):
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post