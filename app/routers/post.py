
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy import func

# connects to app in main.py
router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              user : int = Depends(oauth2.get_current_user),
              limit : int = 10, skip: int = 0, search : Optional[str] = ""):
    #cursor.execute(''' SELECT * FROM posts''')
    #posts = cursor.fetchall()
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),
                 user : int = Depends(oauth2.get_current_user)):
    '''
        Function has a dependancy on get_current_user.
        This insures only logged in users able to post.
    '''
    
    
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #               RETURNING *""",
    #               (post.title, post.content, post.published ))
    #new_post = cursor.fetchone()
    #conn.commit()
    print(user.email)
    new_post = models.Post(owner_id = user.id, **post.dict()) # unpacks dictionary in required format
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrive the new post we committed and store back into new_post
    return new_post

# title str, content str

# get specific post
@router.get("/{id}", response_model=schemas.PostOut)
# forces id to be an integer
def get_post(id: int, db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * from posts where id = %s """, (str(id),))
    #post = cursor.fetchone()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    
    # if the id does not exist
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    
    
    return post

@router.delete("/{id}", response_model=schemas.Post)
def delete_post(id: int,  db: Session = Depends(get_db),status_code=status.HTTP_204_NO_CONTENT,
                user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE from posts where id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone() 
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")
        
    if user.id != post.owner_id:      
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Not authorized to perform requested action!")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts set title = %s, content = %s, published = %s where id = %s Returning *""",
    #               (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")
    
    if user.id != post.owner_id:      
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Not authorized to perform requested action!")
    
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return  post_query.first()