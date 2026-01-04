#main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class User(BaseModel):
    username: str
    email: str
    age: int

retry_count =0
max_count = 5


while retry_count <= max_count:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='1411', 
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2) 
        retry_count+=1


@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users


@app.post("/users", status_code=201)
def create_user(user: User):
    cursor.execute("""
        INSERT INTO users (username, email, age) 
        VALUES (%s, %s, %s) RETURNING *
    """, (user.username, user.email, user.age))
    
    new_user = cursor.fetchone()
    
    conn.commit() 
    
    return new_user


@app.get("/users/{id}")
def get_user(id: int):
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user


@app.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    cursor.execute("DELETE FROM users WHERE id = %s RETURNING *", (str(id),))
    deleted_user = cursor.fetchone()
    
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conn.commit()
    return 


@app.put("/users/{id}")
def update_user(id: int, user: User):
    cursor.execute("""
        UPDATE users 
        SET username = %s, email = %s, age = %s 
        WHERE id = %s 
        RETURNING *
    """, (user.username, user.email, user.age, str(id)))
    
    updated_user = cursor.fetchone()
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    conn.commit()
    
    return updated_user
