from flask import Flask, render_template
from flask import request
from flask import jsonify
from cls_users import Users

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add():
    a = request.form.get("new-name", 0, type=str)
    users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    users.append({"name":a})
    return render_template("list_users.html", users=users)

# @app.route("/room")
# def room():
#     users=[{"name":"a"},{"name":"a"},{"name":"a"}]
#     return render_template("room.html", users=users)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html", forward_message="")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/api/room', methods=['GET', 'POST'])
def room():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
       return "Error 404: Room not found."

    a = Users("jakub")

    users=[{"name":"a"},{"name":"a"},{"name":"a"}]

    return render_template("room.html", room_id=id, users=users)

if __name__ == "__main__":
    app.run(debug=True)