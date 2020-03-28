from flask import Flask, render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add", methods=["POST"])
def add():
    a = request.form.get("new-name", 0, type=str)
    users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    users.append({"name":a})
    return render_template("list_users.html", users=users)

@app.route("/room")
def room():
    users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    return render_template("room.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)