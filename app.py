from flask import Flask, render_template, request, redirect, url_for
from cruds.device import read_all_devices, create_device

app = Flask(__name__)

@app.route("/")
def index():
    device_list = read_all_devices()
    return render_template("index.html", devices=device_list)

@app.route("/add-device", methods=["GET", "POST"])
def add_device():
    if request.method == "POST":
        name = request.form["name"]
        active_time = int(request.form["active_time"])
        break_time = int(request.form["break_time"])
        sets = int(request.form["sets"])
        picture_path = request.form["picture_path"]
        create_device(name, active_time, break_time, sets, picture_path)
        return redirect(url_for("index"))
    return render_template("add_device.html")

if __name__ == "__main__":
    app.run(debug=True)
    