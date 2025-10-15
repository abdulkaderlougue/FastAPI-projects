import json
import random
from fastapi import FastAPI, Response, status, HTTPException
import uvicorn
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    # phone_number:

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None # Optional[int] = None

JSON_DB = 'posts.json'

with open(JSON_DB, 'r') as f:
    my_posts = json.load(f)

# my_posts = []

api = FastAPI()

def find_post(id):
    posts = read_posts()

    for post in posts:
        if post['id'] == id:
            return {"detail":post}

def read_posts():
    """
    get the posts from the json db and return all the posts
    """
    try:
        with open(JSON_DB, 'r') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print("File not found")
        posts = []
    except json.JSONDecodeError:
        print(f"Warning: '{JSON_DB}' is empty or contains invalid JSON. Starting with an empty list.")
        posts = []
    
    return posts

def find_post_index(id):
    """
    Take id of a post and return the index of the post in the json database
    return None if the post does not exist
    """
    posts = read_posts()
    # print("==========",type(posts[0]))
    for idx, post in enumerate(posts):
        if post['id'] == id:
            return idx
    return None
        
def remove_post(id):
    idx = find_post_index(id)
    if not idx:
        # if the index does not exist
        return False
    
    try:
        with open(JSON_DB, 'r') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        # file not found, start with an empty list
        return False
    except json.JSONDecodeError:
        # file is empty or has invalid JSON
        print(f"Warning: '{JSON_DB}' is empty or contains invalid JSON. Starting with an empty list.")
        return False
    
    # delete the post
    old_data.pop(idx)

    # write back to the json db
    with open(JSON_DB, 'w') as f:
        json.dump(old_data, f, indent=3)

    
    return True

def update_post_func(updated_post):

    # remove the old post
    is_remove = remove_post(updated_post['id'])
    
    if is_remove:
        # add the updated post 
        write_to_json_db(updated_post)
        return True

    return False


def write_to_json_db(post_dict):
    """
    Add a post to the db
    """
    try:
        with open(JSON_DB, 'r') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        # file not found, start with an empty list
        old_data = []
    except json.JSONDecodeError:
        # file is empty or has invalid JSON
        print(f"Warning: '{JSON_DB}' is empty or contains invalid JSON. Starting with an empty list.")
        old_data = []
    
   
    # append new data to the existing data
    old_data.append(post_dict)
 
    # write back to the json db
    with open(JSON_DB, 'w') as f:
        json.dump(old_data, f, indent=3)


@api.get('/')
async def home():
    return {"message": "Welcome to the social media api"}

@api.get("/posts")
async def get_posts():
    with open(JSON_DB, 'r') as f:
        my_posts = json.load(f)
    return {'data': my_posts}

@api.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post): # payload: dict = Body(...) convert payload to dict
    post_dict = post.model_dump() # convert to dict
    post_dict['id'] = random.randint(1,100000000)
    # my_posts.append(post_dict)

    write_to_json_db(post_dict)
    
    return {'data': post_dict}

@api.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': "post is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    return {'data': post}

@api.delete('/posts/{id}')
async def delete_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Deletion failed! Post with id {id} not found"
        )
    is_deleted = remove_post(id)
    if is_deleted:
        return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Successfully deleted post {id}')
    
    return Response(status_code= status.HTTP_204_NO_CONTENT, content=f'Failed to delete post {id}')

@api.put('/posts/{id}')
async def update_post(id: int, upd_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Deletion failed! Post with id {id} not found")  
    
    # update the post
    post_dict = upd_post.model_dump()
    post_dict["id"] = id
    is_updated = update_post_func(post_dict)

    if is_updated:
        return {"message": "The post has been updated successfully", "data": post_dict}

@api.get('/users')
async def get_users():
    return {'data': 'These are the users'}

@api.get('users/{id}')
async def get_user_by_id(id: int):
    return User

if __name__ == "__main__":
    uvicorn.run(api)