from flask import Flask, render_template, request
import os
import datetime
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


app = Flask(__name__, static_folder="static")



@app.route("/")
def home():
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    log_visit(request)
    img_dir = "/var/www/html1.0/static/pics/"
    images = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.pdf'))]

    return render_template('gallery.html', images = images)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    if request.method == "Post":
        email = request.form["email"]
        with open("subscribers.txt", "a") as file:
            file.write(email + "\n")
        return "Weclome to hell<3"
    return render_template("newsletter.html")

def log_visit(request):
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("visitor.log", "a") as file:
        file.write(f"{timestamp} - {ip}\n")
        file.write(f"{request.remote_addr} visited {request.path} at {request.headers.get('User-Agent')}\n")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
