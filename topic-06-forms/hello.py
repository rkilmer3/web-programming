from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/hello" , methods=["POST"])
def get_hello():
    name = request.form.get("name", None)
    password = request.form.get("password", None)
    print([name, password])
    data = {
        "name":name,
        "password":password
    }
    return render_template("hello.html", data=data)