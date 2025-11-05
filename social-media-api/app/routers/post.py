from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from schemas import PostBase, PostCreate, PostResponse
import models, schemas, utils
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from .oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    """ Get all posts """
    # cursor.execute('''SELECT * FROM posts ''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # with open(JSON_DB, 'r') as f:
    #     my_posts = json.load(f)
    return posts # {'data': posts}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)): # payload: dict = Body(...) convert payload to dict
    """ Create a post, user needs to be authenticated to do so"""
    # post_dict = post.model_dump() # convert to dict
    # post_dict['id'] = random.randint(1,100000000)
    # # my_posts.append(post_dict)

    # write_to_json_db(post_dict)

    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
    #                (post.title, post.content, post.published)
    #             )
    # new_post = cursor.fetchone()
    # # commit the change to the db
    # conn.commit()

    # create the new post with the sqlalchemy model, passing the kwards args to parse the args from the dict
    print("Login user ID for create post: ",current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post) # add the post to the db

    db.commit() # save the change
    db.refresh(new_post) # refresh the post and return it
    return new_post #{'data': new_post}

@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    # post = find_post(id)
    # cursor.execute(''' SELECT * FROM posts Where id= %s ''', (str(id),)) # the extra comma fixed issue where when id is more than 9
    # post = cursor.fetchone()

    print("Login User ID for get post: ", current_user.id)
    post = db.query(models.Post).filter(models.Post.id == id).first()  # or below
    # post = db.query(models.Post).get(id)

    # print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': "post is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    return post #{'data': post}

@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    # post = find_post(id)

    # cursor.execute('''DELETE  FROM posts WHERE id= %s RETURNING  *''', (str(id),))
    # deleted_post = cursor.fetchone()
    print("Login User ID for delete: ", current_user.id)
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    # print(deleted_post)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Deletion failed! Post with id {id} not found"
        )
    
    # only the owner can delete
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f"Not authorized to perform requested action"
        )
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    # conn.commit()
    # is_deleted = remove_post(id)
    # if is_deleted:
    return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Successfully deleted post {id}')
    
    # return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Failed to delete post {id}')

@router.put('/{id}', response_model=PostResponse)
async def update_post(id: int, upd_post: PostBase, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    # post = find_post(id)

    # cursor.execute('''UPDATE posts SET title = %s, content= %s, published=%s WHERE id=%s RETURNING *''', 
    #                (upd_post.title, upd_post.content, upd_post.published,str(id) ))
    # updated_post = cursor.fetchone()
    print("Login User ID for update: ", current_user.id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Update failed! Post with id {id} not found")  
    
    # only the owner can update
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f"Not authorized to perform requested action"
        )
    post_query.update(upd_post.model_dump(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first() # {"message": "The post has been updated successfully", "data": post_query.first()}
