# Create a Mongita database with movie information
import json
from mongita import MongitaClientDisk

quotes_data = [
    {"text": "I'm hungry. When's lunch?", "author": "Dorothy","owner":"Greg"},
    {"text": "You threw that ball. You go get it.", "author": "Suzy", "owner":"Dorothy"},
]

# create a mongita client connection
client = MongitaClientDisk()

# create a movie database
quotes_db = client.quotes_db

# create a quotes collection
quotes_collection = quotes_db.quotes_collection

# empty the collection
quotes_collection.delete_many({})

# put the quotes in the database
quotes_collection.insert_many(quotes_data)

# make sure the quotes are there
print(quotes_collection.count_documents({}))

###################
# Create a comments database
comments_db = client.comments_db

# Create a comments collection
comments_collection = comments_db.comments_collection

# Empty the collection
comments_collection.delete_many({})

# Sample comments data
comments_data = [
    {"text": "This is a comment.", "user": "Alice", "quote_id": 1},
    {"text": "This is another comment.", "user": "Bob", "quote_id": 2},
]

# Put the comments in the database
comments_collection.insert_many(comments_data)

# Make sure the comments are there
print(comments_collection.count_documents({}))

# Function to add a comment to a quote
def add_comment(quote_id, comment):
    quote = quotes_collection.find_one({"_id": quote_id})
    if quote and not quote.get('comments_prohibited', False):
        comments_collection.insert_one(comment)
    else:
        print("Comments are prohibited on this quote.")

# Function to prohibit comments on a quote
def prohibit_comments(quote_id):
    quotes_collection.update_one({"_id": quote_id}, {"$set": {"comments_prohibited": True}})

# Function to delete a comment
def delete_comment(comment_id):
    comments_collection.delete_one({"_id": comment_id})