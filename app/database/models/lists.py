from app import db

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship


DATE_FORMAT = "%Y-%m-%d %H:%M"


class ToDoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_complete = db.Column(db.Boolean)
    tasks = relationship("Task")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_complete": self.is_complete,
        }

    def __repr__(self):
        return "<ToDoList {} {}>".format(self.id, self.name, self.is_complete)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    status = db.Column(Enum("pending", "done", name="status"))
    due_date = db.Column(db.DateTime())
    list_id = db.Column(db.Integer, ForeignKey("todolist.id"))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date.strftime(DATE_FORMAT) if self.due_date else None,
        }

    def __repr__(self):
        return "<Task {} {} {} {} {} {}>".format(
            self.id,
            self.list_id,
            self.title,
            self.description,
            self.status,
            self.due_date,
        )
