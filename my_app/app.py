from flask import Flask, render_template, request, redirect, url_for

from db_config import db, User, Task


app = Flask(__name__)


# Create database tables
db.create_tables()


# --------------------------------
# HOME
# --------------------------------

@app.route("/")
def home():

    session = db.SessionLocal()

    try:

        # Get all tasks
        tasks = (
            session.query(Task)
            .order_by(Task.id.desc())
            .all()
        )

        # Get all users
        users = (
            session.query(User)
            .all()
        )

        return render_template(
            "home.html",
            tasks=tasks,
            users=users
        )

    finally:

        session.close()


# --------------------------------
# ADD TASK
# --------------------------------

@app.route("/add", methods=["POST"])
def add_task():

    task_name = request.form.get("task_name")
    task_date = request.form.get("task_date")
    status = request.form.get("status")
    user_id = request.form.get("user_id")

    session = db.SessionLocal()

    try:

        task = Task(
            task_name=task_name,
            task_date=task_date,
            status=status,
            user_id=int(user_id) if user_id else None
        )

        session.add(task)
        session.commit()

    finally:

        session.close()

    return redirect(url_for("home"))


# --------------------------------
# DELETE TASK
# --------------------------------

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    session = db.SessionLocal()

    try:

        task = (
            session.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

        if task:
            session.delete(task)
            session.commit()

    finally:

        session.close()

    return redirect(url_for("home"))


# --------------------------------
# RUN
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)