import json
from flask import Flask, request
from flask_cors import CORS
from flask.json import jsonify
from pymongo import MongoClient
from bson import json_util

# CORS enabled

app = Flask(__name__)
CORS(app)

# DB Connection

try:
    client = MongoClient(
        "mongodb+srv://practices-db-user:rQPhbVDz2rMrsjGF@cluster0.jyzwq.mongodb.net/practices-db?retryWrites=true&w=majority")

    collection = client["practices-db"]["practices"]

    print("Connection established")

except Exception as e:
    print(e)


# Routes


@app.route("/practices", methods=['GET', 'POST'])
def practices():

    if request.method == 'GET':

        return find_all()

    elif request.method == 'POST':

        return create(request)


@app.route("/practices/<id>", methods=['GET', 'PUT', 'DELETE'])
def practice(id):

    if request.method == 'GET':

        return find_one(id)

    elif request.method == 'PUT':

        return update_one(request, id)

    elif request.method == 'DELETE':

        return remove_one(id)


# Controllers


def create(request):

    data = request.get_json()

    # Object model or dictionary in python

    obj = {

        "title": data["title"],

        "problem": data["problem"],

        "point": data["point"],

        "level": data["level"],

        "language": data["language"],

        "input": data["input"],

        "expected_output": data["expected_output"]

    }

    collection.insert_one(obj)

    return jsonify({
        "success": "Practice successfully created!"
    })


def find_all():

    response = []

    for i in collection.find():
        response.append(i)

    return json.dumps(response, default=json_util.default)


def find_one(id):

    response = collection.find_one({"_id": id})

    return response


def update_one(request, id):

    data = request.get_json()

    query = {"_id": id}

    collection.update_one(query, {"$set": data})

    return jsonify({
        "success": "(obj_id: {}) practice edited!".format(id)
    })


def remove_one(id):

    collection.delete_one({"_id": id})

    return jsonify({
        "success": "(obj_id: {}) practice removed!".format(id)
    })
