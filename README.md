# Todo API
This is an API for creating lists todo lists that contain tasks. To try it out locally, follow these steps:

## Setup

1. [Install docker](https://docs.docker.com/get-docker/)
2. `git clone https://github.com/emtwo/todo.git`
3. `cd todo`
4. `docker-compose build`
5. `docker-compose up`

## Usage
These steps will start up a server running a REST API. Here are some examples of how you can try it out with curl:

###### Create a New List
`curl 0.0.0.0:5000/create/list/ -d '{"name": "My Todo List"}' -H 'Content-Type: application/json'`

###### Show All Lists
`curl 0.0.0.0:5000/lists/`

###### Create a list item for a given list
`curl 0.0.0.0:5000/create/item/ -d '{"title": "Buy Milk", "description": "pick up milk at the grocery store", "due_date":"2021-02-23 05:00", "list_id": 1}' -H 'Content-Type: application/json'`

###### Show all items in a given list
`curl 0.0.0.0:5000/list/1`

###### Update a given list's name
`curl 0.0.0.0:5000/list/1 -d '{"name": "My New List Name"}' -H 'Content-Type: application/json'`

###### Update a given item
`curl 0.0.0.0:5000/item/1 -d '{"title": "Buy Milk from Loblaws"}' -H 'Content-Type: application/json'`
`curl 0.0.0.0:5000/item/1 -d '{"status": "done"}' -H 'Content-Type: application/json'`

###### Delete a list and all of its items
`curl -X DELETE curl 0.0.0.0:5000/list/2`

###### Delete an item
`curl -X DELETE curl 0.0.0.0:5000/list/2`

###### Track all items with a given status (e.g. pending)
`curl 0.0.0.0:5000/item/pending`

###### Look up the next X due items
`curl 0.0.0.0:5000/next_due/2`