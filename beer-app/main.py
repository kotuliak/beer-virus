from flask import Flask, render_template, request, redirect
from cls_room import Room

app = Flask(__name__)

open_rooms = []


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/api/room', methods=['GET', 'POST'])
def room():
    if 'id' in request.args:
        id = int(request.args['id'])
        for room in open_rooms:
            if id == room.id:
                if 'name' in request.args:
                    name = str(request.args['name'])
                else:
                    return "Error 404: User not found."

                return render_template("room.html", room_id=id, users=open_rooms[0].users, your_user=open_rooms[0].get_user(name))

    return "Error 404: Room not found."

@app.route('/create_new_room', methods=['POST'])
def create_new_room():
    new_room = Room()
    open_rooms.append(new_room)
    return redirect("/api/room?id=" + str(new_room.id))


@app.route('/join_room', methods=['POST'])
def join_room():
    room_id = request.form['room-id']
    return redirect("/api/room?id=" + room_id)


@app.route("/add", methods=["POST"])
def add():
    a = request.form.get("new-name", 0, type=str)
    users = [{"name": "a"}, {"name": "a"}, {"name": "a"}]
    users.append({"name": a})
    return render_template("list_users.html", users=users)

@app.route("/add_location", methods=["POST"])
def add_location():
    print(eval(request.data))
    # a = request.form.get("new-name", 0, type=str)
    # users=[{"name":"a"},{"name":"a"},{"name":"a"}]
    # users.append({"name":a})
    open_rooms[0].get_user(eval(request.data)['name']).location = eval(request.data)['location']
    return render_template("user.html", your_user=open_rooms[0].get_user(eval(request.data)['name']))


if __name__ == "__main__":
    app.run(debug=True)
