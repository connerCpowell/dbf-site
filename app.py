# from flask import Flask, render_template, request, jsonify, url_for
# import os
# import re 
# import sqlite3
# import datetime
# import logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG)


# app = Flask(__name__, static_folder="static")

# img_dir = "/var/www/html1.0/static/pics/"
# DB_FILE = "emails.db"

# def init_db():
#     if not os.path.exists(DB_FILE):
#         conn = sqlite3.connect(DB_FILE)
#         cursor = conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             email TEXT UNIQUE NOT NULL
#                           )''')
#         conn.commit()
#         conn.close()
    
# init_db()

# def is_valid_email(email):
#     return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

# def get_images():
#     return sorted(os.listdir(img_dir))

# @app.route("/")
# def home():
#     return render_template("about.html")

# @app.route("/gallery")
# def gallery():
#     log_visit(request)
#     images = get_images()[:9]
#     return render_template('gallery.html', images = images)

# @app.route("/gallery/load_more")
# def load_more():
#     page = int(request.args.get('page', 1))
#     images = get_images()
#     start_idx = page * 9
#     end_idx = (page + 1) * 9
#     next_batch = images[start_idx:end_idx]

#     print(f"start:{start_idx} end:{end_idx}")
#     print(f"next: {next_batch}")

#     if not next_batch:
#         return jsonify({'images' : []})

#     return jsonify({'images': [url_for('static', filename=f'pics/{img}') for img in next_batch]})

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/signup", methods=["GET"])
# def signup():
#     print(url_for('subscribe')) 
#     return render_template("signup.html")

# @app.route("/subscribe", methods=["POST"])
# def subscribe():
#     print("Subscribe route triggered") 
#     data = request.get_json()
#     email = data.get("email", "").strip()

#     if not email or not is_valid_email(email):
#         return jsonify({"message": "Invalid email address"}), 400

#     try:
#         conn = sqlite3.connect(DB_FILE)
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO emails (email) VALUES (?)", (email,))
#         conn.commit()
#         conn.close()

#         # Notify site owner (Optional: Replace with actual email sending)
#         with open("new_signups.log", "a") as log_file:
#             log_file.write(f"New signup: {email}\n")

#         return jsonify({"message": "Successfully signed up!"})
#     except sqlite3.IntegrityError:
#         return jsonify({"message": "Email already registered"}), 400
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred"}), 500


# def log_visit(request):
#     ip = request.remote_addr
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open("visitor.log", "a") as file:
#         file.write(f"{timestamp} - {ip}\n")
#         file.write(f"{request.remote_addr} visited {request.path} at {request.headers.get('User-Agent')}\n")


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
