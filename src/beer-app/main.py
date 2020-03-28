from flask import Flask, render_template
from flask import request
from flask import jsonify
from cls_users import Users
from cls_room import Room

app = Flask(__name__)

rooms = []
rooms.append(Room())
rooms[0].create_user("Mato")
rooms[0].create_user("Jakub")
rooms[0].create_user("Miso")
rooms[0].create_user("Luca")

@app.route("/add", methods=["POST"])
def add():
    a = request.form.get("new-name", 0, type=str)
    users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    users.append({"name":a})
    return render_template("list_users.html", users=users)

@app.route("/add_location", methods=["POST"])
def add_location():
    print(eval(request.data))
    # a = request.form.get("new-name", 0, type=str)
    # users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    # users.append({"name":a})
    rooms[0].get_user(eval(request.data)['name']).location = eval(request.data)['location']
    return render_template("user.html", your_user=rooms[0].get_user(eval(request.data)['name']))

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

    if 'name' in request.args:
        name = str(request.args['name'])
    else:
       return "Error 404: User not found."

    return render_template("room.html", room_id=id, users=rooms[0].users, your_user=rooms[0].get_user(name))

if __name__ == "__main__":
    app.run(debug=True)