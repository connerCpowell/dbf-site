from flask import Flask, render_template, request, jsonify, url_for
import os
import datetime
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


app = Flask(__name__, static_folder="static")

img_dir = "/var/www/html1.0/static/pics/"



def get_images():
    return sorted(os.listdir(img_dir))

@app.route("/")
def home():
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    log_visit(request)
    images = get_images()[:9]
    return render_template('gallery.html', images = images)

@app.route("/gallery/load_more")
def load_more():
    page = int(request.args.get('page', 1))
    images = get_images()
    start_idx = page * 9
    end_idx = (page + 1) * 9
    next_batch = images[start_idx:end_idx]

    print(f"start:{start_idx} end:{end_idx}")
    print(f"next: {next_batch}")

    if not next_batch:
        return jsonify({'images' : []})

    return jsonify({'images': [url_for('static', filename=f'pics/{img}') for img in next_batch]})

@app.route("/about")
def about():
    return render_template("about.html")


def log_visit(request):
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("visitor.log", "a") as file:
        file.write(f"{timestamp} - {ip}\n")
        file.write(f"{request.remote_addr} visited {request.path} at {request.headers.get('User-Agent')}\n")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
