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
    if 'room_id' in request.form:
        print(request.form)
        id = int(request.form['room_id'])
        for room in open_rooms:
            if id == room.id:
                if 'user_name' in request.form:
                    user_name = request.form['user_name']
                    your_user = room.get_user(user_name)
                    if your_user is None:
                        your_user = room.create_user(user_name)
                    return render_template("room.html", room_id=id, your_user=your_user, users=room.users.values())
                else:
                    return render_template("join_room.html", room_id=id)
    elif 'room_id' in request.args:
        print(request.args)
        id = int(request.args['room_id'])
        for room in open_rooms:
            if id == room.id:
                if 'user_name' in request.args:
                    user_name = request.args['user_name']
                    your_user = room.get_user(user_name)
                    if your_user is None:
                        your_user = room.create_user(user_name)
                    return render_template("room.html", room_id=id, your_user=your_user, users=room.users.values())
                else:
                    return render_template("join_room.html", room_id=id)

    return "Error 404: Room not found."


@app.route('/create_new_room', methods=['POST'])
def create_new_room():
    new_room = Room()
    open_rooms.append(new_room)
    return redirect("/join_room?room_id=" + str(new_room.id))

@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if 'room_id' in request.args:
        room_id = request.args['room_id']
    elif 'room_id' in request.form:
        room_id = request.form['room_id']

    return render_template("join_room.html", room_id=room_id)

@app.route("/add_location", methods=["POST"])
def add_location():
    print(eval(request.data))
    for room in open_rooms:
        if int(eval(request.data)['roomid']) == room.id:
            room.get_user(eval(request.data)['name']).location = eval(request.data)['location']
            room.assign_location(eval(request.data)['name'], eval(request.data)['location'])
            return render_template("user.html", your_user=room.get_user(eval(request.data)['name']))


if __name__ == "__main__":
    app.run(debug=True)
