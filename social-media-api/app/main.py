
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import uvicorn
import models
from database import engine, get_db
from schemas import PostBase, PostCreate, PostResponse, User
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

@api.get('/')
async def home():
    return {"message": "Welcome to the social media api"}

@api.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts ''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # with open(JSON_DB, 'r') as f:
    #     my_posts = json.load(f)
    return posts # {'data': posts}

@api.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_posts(post: PostCreate, db: Session = Depends(get_db)): # payload: dict = Body(...) convert payload to dict
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
    new_post = models.Post(**post.model_dump())

    db.add(new_post) # add the post to the db

    db.commit() # save the change
    db.refresh(new_post) # refresh the post and return it
    return new_post #{'data': new_post}

@api.get("/posts/{id}", response_model=PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)
    # cursor.execute(''' SELECT * FROM posts Where id= %s ''', (str(id),)) # the extra comma fixed issue where when id is more than 9
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()  # or below
    # post = db.query(models.Post).get(id)

    # print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': "post is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    return post #{'data': post}

@api.delete('/posts/{id}')
async def delete_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)

    # cursor.execute('''DELETE  FROM posts WHERE id= %s RETURNING  *''', (str(id),))
    # deleted_post = cursor.fetchone()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    # print(deleted_post)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Deletion failed! Post with id {id} not found"
        )
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    # conn.commit()
    # is_deleted = remove_post(id)
    # if is_deleted:
    return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Successfully deleted post {id}')
    
    # return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Failed to delete post {id}')

@api.put('/posts/{id}', response_model=PostResponse)
async def update_post(id: int, upd_post: PostBase, db: Session = Depends(get_db)):
    # post = find_post(id)

    # cursor.execute('''UPDATE posts SET title = %s, content= %s, published=%s WHERE id=%s RETURNING *''', 
    #                (upd_post.title, upd_post.content, upd_post.published,str(id) ))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Update failed! Post with id {id} not found")  
    
    post_query.update(upd_post.model_dump(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first() # {"message": "The post has been updated successfully", "data": post_query.first()}

@api.get('/users')
async def get_users():
    return {'data': 'These are the users'}

@api.get('users/{id}')
async def get_user_by_id(id: int):
    return User

if __name__ == "__main__":
    uvicorn.run(api)