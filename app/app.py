import json
from tabulate import tabulate

from flask import request, make_response, abort

import datetime

from . import create_app
from .database.models.lists import db, ToDoList, Task

app = create_app()
DATE_FORMAT = "%Y-%m-%d %H:%M"


@app.route("/item/<status>", methods=["GET"])
def get_by_status(status):
    items = Task.query.filter(Task.status == status).all()
    result = [
        {
            "list_name": ToDoList.query.filter(ToDoList.id == item.list_id).first().name,
            **item.serialize(),
        }
        for item in items
    ]
    return make_response(json.dumps(result))


@app.route("/next_due/<count>", methods=["GET"])
def get_next_due(count):
    items = (
        Task.query.filter(Task.due_date != None)
        .order_by(Task.due_date.desc())
        .limit(count)
        .all()
    )
    result = [
        {
            "list_name": ToDoList.query.filter(ToDoList.id == item.list_id)
            .first()
            .name,
            **item.serialize(),
        }
        for item in items
    ]
    return make_response(json.dumps(result))


@app.route("/lists/", methods=["GET"])
def get_lists():
    lists = ToDoList.query.all()
    list_items = [[todolist.name, todolist.id] for todolist in lists]
    print(tabulate(list_items, headers=["Name", "ID"]))
    return make_response(json.dumps(list_items))


@app.route("/list/<list_id>", methods=["GET"])
def get_list(list_id):
    list_data = ToDoList.query.filter(ToDoList.id == list_id).first()

    if list_data is None:
        return abort(404, description=f"List ID {list_id} does not exist!")

    list_items = Task.query.filter(Task.list_id == list_id)

    result = {
        "id": list_data.id,
        "name": list_data.name,
        "complete": list_data.is_complete,
        "items": [item.serialize() for item in list_items],
    }
    return make_response(json.dumps(result))


@app.route("/list/<list_id>", methods=["POST"])
def update_list(list_id):
    data = request.get_json()

    list_data = ToDoList.query.filter(ToDoList.id == list_id)

    if list_data.first() is None:
        return abort(404, description=f"List ID {list_id} does not exist!")

    if not set(data.keys()) <= set(ToDoList.__table__.columns.keys()):
        return abort(400, description=f"Non-existant columns cannot be updated!")

    list_data.update(data)
    db.session.commit()
    return make_response(f"Update of list with ID {list_id} successfully completed!")


@app.route("/item/<item_id>", methods=["POST"])
def update_item(item_id):
    data = request.get_json()

    item_data = Task.query.filter(Task.id == item_id)

    if item_data.first() is None:
        return abort(404, description=f"Task ID {task_id} does not exist!")

    if not set(data.keys()) <= set(Task.__table__.columns.keys()):
        return abort(400, description=f"Non-existant columns cannot be updated!")

    item_data.update(data)
    db.session.commit()
    return make_response(f"Update of task with ID {item_id} successfully completed!")


@app.route("/list/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    todolist = ToDoList.query.filter(ToDoList.id == list_id).first()

    if todolist is None:
        return abort(404, description=f"List ID {list_id} does not exist!")

    # Delete all the list items before deleting the list
    list_items = Task.query.filter(Task.list_id == list_id)
    for item in list_items:
        db.session.delete(item)

    db.session.delete(todolist)
    db.session.commit()

    return make_response(f"{todolist} successfully deleted!")


@app.route("/item/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Task.query.filter(Task.id == item_id).first()

    if item is None:
        return abort(404, description=f"Item ID {item_id} does not exist!")

    db.session.delete(item)
    db.session.commit()

    return make_response(f"{item} successfully deleted!")


@app.route("/create/item/", methods=["POST"])
def create_item():
    """
    Create a list item.

    POST payload params:
    due_date -- optional -- in the format YYYY-MM-DD HH:MM
    """

    data = request.get_json()
    title = data.get("title", None)
    description = data.get("description", None)
    due_date = data.get("due_date", None)
    list_id = data.get("list_id", None)

    if title is None or list_id is None:
        return abort(400, description=f"List ID and title cannot be null!")

    list_to_append = ToDoList.query.filter(ToDoList.id == list_id).first()

    if list_to_append is None:
        return abort(404, description=f"List ID {list_id} does not exist!")

    if due_date is not None:
        try:
            due_date = datetime.datetime.strptime(due_date, DATE_FORMAT)
        except ValueError:
            return abort(400, description=f"Date format must be YYYY-MM-DD HH:MM")

    new_item = Task(
        title=title,
        description=description,
        status="pending",
        due_date=due_date,
        list_id=list_id,
    )
    db.session.add(new_item)
    db.session.commit()

    return make_response(json.dumps(new_item.serialize()))


@app.route("/create/list/", methods=["POST"])
def create_list():
    data = request.get_json()
    name = data.get("name", None)

    if name is None:
        return make_response(f"Name can't be null!")

    new_list = ToDoList(name=name, is_complete=False)
    db.session.add(new_list)
    db.session.commit()
    return make_response(json.dumps(new_list.serialize()))
