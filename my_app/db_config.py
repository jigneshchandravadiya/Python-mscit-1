import os

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    # User -> Tasks relationship
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    task_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    task_date: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # Task -> User relationship
    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )


class Database:

    def __init__(self):

        # Flask project folder
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # instance folder
        instance_dir = os.path.join(
            base_dir,
            "instance"
        )

        # instance folder ન હોય તો create કરશે
        os.makedirs(
            instance_dir,
            exist_ok=True
        )

        # Database location
        self.database_name = os.path.join(
            instance_dir,
            "todo.db"
        )

        # SQLAlchemy SQLite URL
        database_url = f"sqlite:///{self.database_name}"

        # Engine
        self.engine = create_engine(
            database_url,
            echo=False
        )

        # Session
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

    def create_tables(self):

        # users અને tasks બંને tables create થશે
        Base.metadata.create_all(
            self.engine
        )

        # Static user create કરવો
        session = self.SessionLocal()

        try:

            existing_user = session.query(User).filter_by(
                email="cjahir@2120"
            ).first()

            if existing_user is None:

                user = User(
                    name="jignesh",
                    email="cjahir@2120"
                )

                session.add(user)
                session.commit()

        finally:

            session.close()


# Object
db = Database()
