from flask import Flask, render_template, request, jsonify, url_for
import os, re, sqlite3, datetime, logging

app = Flask(__name__, static_folder="static")
logging.basicConfig(filename='app.log', level=logging.DEBUG)

DB_FILE = "emails.db"
img_dir = os.path.join(app.static_folder, "pics")   # <-- improved

# ------------------ DB Initialization ------------------ #

def init_db():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL
                )
            """)

init_db()

# ------------------ Helper Functions ------------------ #

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def get_images_grouped():
    grouped = {}

    if not os.path.exists(img_dir):
        return grouped

    for folder in sorted(os.listdir(img_dir)):
        fpath = os.path.join(img_dir, folder)
        if os.path.isdir(fpath):
            images = [
                {
                    "file": img,
                    "url": url_for("static", filename=f"pics/{folder}/{img}")
                }
                for img in sorted(os.listdir(fpath))
                if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            ]
            grouped[folder] = images

    return grouped

def get_images():
    all_images = []
    pics_root = os.path.join(app.static_folder, "pics")

    for root, dirs, files in os.walk(pics_root):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Build path relative to static folder (no "pics/pics/" duplication)
                rel_path = os.path.relpath(os.path.join(root, f), app.static_folder)
                rel_path = rel_path.replace("\\", "/")  # Windows safe
                all_images.append(rel_path)

    return sorted(all_images)

def log_visit(request):
    with open("visitor.log", "a") as file:
        file.write(f"{datetime.datetime.now()} - {request.remote_addr} - {request.path}\n")

# ------------------ Routes ------------------ #

@app.route("/")
def home():
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    log_visit(request)
    print("\n======== DEBUG: Entered /gallery route ========")
    print("img_dir =", img_dir)
    print("os.path.exists(img_dir) =", os.path.exists(img_dir))

    images = get_images()
    print("Found images:", images[:3], "...")

    return render_template("gallery.html")

@app.route('/gallery/load_more')
def load_more():
    page = int(request.args.get('page', 1))
    images_per_page = 12

    all_images = get_images()

    start = (page - 1) * images_per_page
    end = start + images_per_page

    # Convert to web URLs
    image_urls = ["/static/" + path for path in all_images[start:end]]

    return jsonify({
        'images': image_urls,
        'has_more': len(all_images) > end
    })

# @app.route("/view/<path:image_path>")
# def view_image(image_path):
#     return render_template("view.html", image_path=image_path)

@app.route("/view/<path:filename>")
def image_page(filename):
    display_name = filename.split("/")[-1]
    name_wo_ext = os.path.splitext(display_name)[0]

    # Build prev/next navigation based on the list of images.
    # `get_images()` returns paths like 'pics/2025-01/JOE.jpg', but the
    # route `filename` parameter is '2025-01/JOE.jpg'. Normalize by
    # stripping the leading 'pics/' so we can compare and return
    # prev/next in the same form the route expects.
    images = get_images()
    normalized = [p[5:] if p.startswith('pics/') else p for p in images]

    prev_img = None
    next_img = None
    try:
        idx = normalized.index(filename)
        if idx > 0:
            prev_img = normalized[idx - 1]
        if idx < len(normalized) - 1:
            next_img = normalized[idx + 1]
    except ValueError:
        # filename not found in list -- keep prev/next as None
        pass

    return render_template(
        "image_view.html",
        filename=name_wo_ext,
        filepath=filename,
        prev_img=prev_img,
        next_img=next_img
    )

# legacy/unused helper removed

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email", "").strip()

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email"}), 400

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO emails (email) VALUES (?)", (email,))
        return jsonify({"message": "Successfully signed up!"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already registered"}), 400

# ------------------ Run ------------------ #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
