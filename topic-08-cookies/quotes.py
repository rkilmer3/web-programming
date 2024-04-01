from flask import Flask, render_template, request, make_response, redirect
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# create a mongita client connection
client = MongitaClientDisk()

# open the quotes database
quotes_db = client.quotes_db

import uuid

# Generate a random UUID (GUID-like)
session_key = uuid.uuid4()

print(session_key)


@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
    number_of_visits = int(request.cookies.get("number_of_visits", "0"))
    # open the quotes collection
    quotes_collection = quotes_db.quotes_collection
    # load the data
    data = list(quotes_collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
        item["object"] = ObjectId(item["_id"])
    # display the data
    html = render_template("quotes.html", data=data, number_of_visits=number_of_visits, session_id=session_id)
    response = make_response(html)
    response.set_cookie("number_of_visits", str(number_of_visits + 1))
    response.set_cookie("session_id", session_id)
    return response

@app.route("/login", methods=["GET"])
def get_login():
    response = make_response("Logged in.")
    session_id = str(uuid.uuid4())
    response.set_cookie("session_id", session_id)
    return response

@app.route("/logout", methods=["GET"])
def get_logout():
    response = make_response("Logged out.")
    response.delete_cookie("session_id")
    return response


@app.route("/add", methods=["GET"])
def get_add():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
    return render_template("add_quote.html")


@app.route("/add", methods=["POST"])
def post_add():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
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
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
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
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
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
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return "You are not logged in."
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # delete the item
        quotes_collection.delete_one({"_id": ObjectId(id)})
    # return to the quotes page
    return redirect("/quotes")
