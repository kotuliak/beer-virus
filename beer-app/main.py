from flask import Flask, render_template, request, url_for
from cls_room import Room

app = Flask(__name__)

open_rooms = []


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/room', methods=['GET', 'POST'])
def room():
    try:
        if len(request.form) == 0 and len(request.args) > 0:
            room_id = int(request.args['room_id'])
            user_name = request.args['user_name']
        elif len(request.args) == 0 and len(request.form) > 0:
            room_id = int(request.form['room_id'])
            user_name = request.form['user_name']
        else:
            raise Exception("Request args or form empty")
    except Exception as e:
        return "<p>An error occurred:</p><p>" + str(e) + "</p><a href=" + url_for('home') + ">Go Back Home</a>"

    for room in open_rooms:
        if room_id == room.id:
            your_user = room.get_user(user_name)
            if your_user is None:
                your_user = room.create_user(user_name)
            return render_template("room.html", room_id=room_id, your_user=your_user, users=room.users.values())

    return "Error 404: Room not found."


@app.route('/create_new_room', methods=['POST'])
def create_new_room():
    new_room = Room()
    open_rooms.append(new_room)
    return render_template("join_room.html", room_id=new_room.id)


@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    room_id = int(request.form['room_id'])

    for room in open_rooms:
        if room_id == room.id:
            return render_template("join_room.html", room_id=room_id)

    return "Error 404: Room not found."


@app.route("/show_users", methods=["POST"])
def show_users():
    print(eval(request.data))
    for room in open_rooms:
        if int(eval(request.data)['roomid']) == room.id:
            return render_template("list_users.html", users=room.users.values())


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
