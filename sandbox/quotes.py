from flask import Flask, render_template, make_response, request, redirect
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# create a mongita client connection
client = MongitaClientDisk()

# open the quotes database
quotes_db = client.quotes_db

import random
import string


def generate_random_string(length):
    # Choose from letters and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string
    random_string = "".join(random.choice(characters) for i in range(length))
    return random_string


# Example: Generate a 10-character random string
print(generate_random_string(10))

import uuid

# Generate a random UUID (GUID-like)
session_key = uuid.uuid4()

print(session_key)


@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    number_of_visits = int(request.cookies.get("number_of_visits", "0"))
    session_id = request.cookies.get("session_id", str(uuid.uuid4()))
    print(f"number of visits {number_of_visits}")
    print(f"session_key {session_key}")
    # open the quotes collection
    quotes_collection = quotes_db.quotes_collection
    # load the data
    data = list(quotes_collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
        item["object"] = ObjectId(item["_id"])
    # display the data
    html = render_template("quotes.html", data=data, session_id=session_id)
    response = make_response(html)
    response.set_cookie("number_of_visits", str(number_of_visits + 1))
    return response


@app.route("/add", methods=["GET"])
def get_add():
    return render_template("add_quote.html")


@app.route("/add", methods=["POST"])
def post_add():
    text = request.form.get("text", "")
    author = request.form.get("author", "")
    if text != "" and author != "":
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # insert the quote
        quote_data = {"text": text, "author": author}
        quotes_collection.insert_one(quote_data)
    # usually do a redirect('....')
    return redirect("/quotes")


@app.route("/edit/<id>", methods=["GET"])
def get_edit(id=None):
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # get the item
        data = quotes_collection.find_one({"_id": ObjectId(id)})
        data["id"] = str(data["_id"])
        return render_template("edit_quote.html", data=data)
    # return to the quotes page
    return redirect("/quotes")


@app.route("/edit", methods=["POST"])
def post_edit():
    _id = request.form.get("_id", None)
    text = request.form.get("text", "")
    author = request.form.get("author", "")
    if _id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # update the values in this particular record
        values = {"$set": {"text": text, "author": author}}
        data = quotes_collection.update_one({"_id": ObjectId(_id)}, values)
    # do a redirect('....')
    return redirect("/quotes")


@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"])
def get_delete(id=None):
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # delete the item
        quotes_collection.delete_one({"_id": ObjectId(id)})
    # return to the quotes page
    return redirect("/quotes")
