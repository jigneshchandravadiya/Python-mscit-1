from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="Todo Management API",
    description="Todo app with Register, Login, Profile and Tasks",
    version="1.0"
)


# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# =====================================================
# USER MODEL
# =====================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(100),
        nullable=False
    )

    tasks = relationship(
        "Todoapp",
        back_populates="user"
    )


# =====================================================
# TODO MODEL
# =====================================================

class Todoapp(Base):

    __tablename__ = "todoapp"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(500)
    )

    priority = Column(
        String(50)
    )

    is_completed = Column(
        Boolean,
        default=False
    )

    due_date = Column(
        Date
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="tasks"
    )


# Create tables
Base.metadata.create_all(bind=engine)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Todo API is running",
        "docs": "/docs",
        "register": "/register",
        "login": "/login"
    }


# =====================================================
# REGISTER
# =====================================================

@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        db.close()

        return {
            "message": "Email already registered"
        }

    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    user_id = user.id

    db.close()

    return {
        "message": "Registration successful",
        "user_id": user_id,
        "name": name,
        "email": email
    }


# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email,
        User.password == password
    ).first()

    if not user:

        db.close()

        return {
            "message": "Invalid email or password"
        }

    result = {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }

    db.close()

    return result


# =====================================================
# USER PROFILE
# =====================================================

@app.get("/profile/{user_id}")
def profile(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        db.close()

        return {
            "message": "User not found"
        }

    result = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    db.close()

    return result


# =====================================================
# UPDATE PROFILE
# =====================================================

@app.put("/profile/{user_id}")
def update_profile(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        db.close()

        return {
            "message": "User not found"
        }

    user.name = name
    user.email = email

    db.commit()

    db.close()

    return {
        "message": "Profile updated successfully",
        "user_id": user_id,
        "name": name,
        "email": email
    }


# =====================================================
# ADD TASK
# =====================================================

@app.post("/tasks/{user_id}")
def add_task(

    user_id: int,

    title: str = Form(...),

    description: str = Form(""),

    priority: str = Form("Medium"),

    due_date: str = Form(...)

):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        db.close()

        return {
            "message": "User not found"
        }

    date_value = datetime.strptime(
        due_date,
        "%Y-%m-%d"
    ).date()

    task = Todoapp(

        title=title,

        description=description,

        priority=priority,

        is_completed=False,

        due_date=date_value,

        user_id=user_id

    )

    db.add(task)

    db.commit()

    db.refresh(task)

    result = {

        "message": "Task added successfully",

        "task": {

            "id": task.id,

            "title": task.title,

            "description": task.description,

            "priority": task.priority,

            "completed": task.is_completed,

            "due_date": str(task.due_date)

        }

    }

    db.close()

    return result


# =====================================================
# GET ALL TASKS
# =====================================================

@app.get("/tasks/{user_id}")
def get_tasks(user_id: int):

    db = SessionLocal()

    tasks = db.query(Todoapp).filter(
        Todoapp.user_id == user_id
    ).all()

    result = []

    for task in tasks:

        result.append({

            "id": task.id,

            "title": task.title,

            "description": task.description,

            "priority": task.priority,

            "completed": task.is_completed,

            "due_date": str(task.due_date)

        })

    db.close()

    return {
        "user_id": user_id,
        "total_tasks": len(result),
        "tasks": result
    }


# =====================================================
# UPDATE TASK
# =====================================================

@app.put("/tasks/{task_id}")
def update_task(

    task_id: int,

    title: str = Form(...),

    description: str = Form(...),

    priority: str = Form(...),

    due_date: str = Form(...)

):

    db = SessionLocal()

    task = db.query(Todoapp).filter(
        Todoapp.id == task_id
    ).first()

    if not task:

        db.close()

        return {
            "message": "Task not found"
        }

    task.title = title

    task.description = description

    task.priority = priority

    task.due_date = datetime.strptime(
        due_date,
        "%Y-%m-%d"
    ).date()

    db.commit()

    db.close()

    return {
        "message": "Task updated successfully",
        "task_id": task_id
    }


# =====================================================
# TOGGLE TASK
# =====================================================

@app.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):

    db = SessionLocal()

    task = db.query(Todoapp).filter(
        Todoapp.id == task_id
    ).first()

    if not task:

        db.close()

        return {
            "message": "Task not found"
        }

    task.is_completed = not task.is_completed

    db.commit()

    status = task.is_completed

    db.close()

    return {

        "message": "Task status changed",

        "task_id": task_id,

        "completed": status

    }


# =====================================================
# DELETE TASK
# =====================================================

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    db = SessionLocal()

    task = db.query(Todoapp).filter(
        Todoapp.id == task_id
    ).first()

    if not task:

        db.close()

        return {
            "message": "Task not found"
        }

    db.delete(task)

    db.commit()

    db.close()

    return {

        "message": "Task deleted successfully",

        "task_id": task_id

    }


# =====================================================
# PENDING TASKS
# =====================================================

@app.get("/tasks/{user_id}/pending")
def pending_tasks(user_id: int):

    db = SessionLocal()

    tasks = db.query(Todoapp).filter(

        Todoapp.user_id == user_id,

        Todoapp.is_completed == False

    ).all()

    result = []

    for task in tasks:

        result.append({

            "id": task.id,

            "title": task.title,

            "priority": task.priority,

            "due_date": str(task.due_date)

        })

    db.close()

    return {
        "pending_tasks": result
    }


# =====================================================
# COMPLETED TASKS
# =====================================================

@app.get("/tasks/{user_id}/completed")
def completed_tasks(user_id: int):

    db = SessionLocal()

    tasks = db.query(Todoapp).filter(

        Todoapp.user_id == user_id,

        Todoapp.is_completed == True

    ).all()

    result = []

    for task in tasks:

        result.append({

            "id": task.id,

            "title": task.title,

            "priority": task.priority,

            "due_date": str(task.due_date)

        })

    db.close()

    return {
        "completed_tasks": result
    }


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )