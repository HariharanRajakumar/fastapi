from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schemas,models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.get('/blog',response_model=List[schemas.ShowBlog],tags=["blog"])
def get_all_blog(db :Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog',status_code=status.HTTP_201_CREATED,tags=["blog"])
def create(req:schemas.Blog,db :Session = Depends(get_db)):
    exist = db.query(models.Blog).filter(models.User.id == req.id)
    if not exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not found")
    new_blog=models.Blog(title=req.title,body=req.body,user_id=req.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["blog"])
def update(id,req:schemas.Blog,db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} NOT FOUND")

    blog.update({'title':req.title,'body':req.body})
    db.commit()
    return req

@router.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=["blog"])
def show_id(id,response:Response,db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} is not available"}
    return blog

@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["blog"])
def delete_blog(id,db :Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'