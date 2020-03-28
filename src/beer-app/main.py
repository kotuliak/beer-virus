from flask import Flask, render_template, request

app = Flask(__name__)

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

    return render_template("room.html", room_id=id)

if __name__ == "__main__":
    app.run(debug=True)