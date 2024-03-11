from flask import Flask, render_template, request
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# create a mongita client connection
client = MongitaClientDisk()

# open the quotes database
quotes_db = client.quotes_db


@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    # data = [
    #     {"text": "I'm hungry. When's lunch?", "author": "Dorothy"},
    #     {"text": "You threw that ball. You go get it.", "author": "Suzy"},
    # ]
    # open the quotes collection
    quotes_collection = quotes_db.quotes_collection
    # load the data
    data = list(quotes_collection.find({}))
    print(data)
    print(data)
    for item in data:
        item["_id"] = str(item["_id"])
        item["object"] = ObjectId(item["_id"])
    print(data)
    return render_template("quotes.html", data=data)

@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"])
def get_delete(id=None):
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # delete the item
#        quotes_collection.delete_one(_id=ObjectId(id))

# TODO: explain the fix to the old code here:
        # data = list(quotes_collection.find({_id:ObjectId(id)}))
        # the key here is to write _Python_ code, not semi-JS
        data = list(quotes_collection.find({"_id":ObjectId(id)}))
        print(data)
# TODO: redirect here! 
    return render_template("quotes.html", data=data)


