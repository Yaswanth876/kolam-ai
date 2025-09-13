import os
import uuid
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from utils import svg_generator

# Config
UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


# --- Helpers ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())[:8]
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{file_id}_{filename}")
        file.save(save_path)

        # Dummy classification
        classification = "Sikku Kolam"
        confidence = 0.87
        features = {"dots": 25, "symmetry": "4-fold"}

        return render_template(
            "results.html",
            image_path=save_path,
            classification=classification,
            confidence=confidence,
            features=features,
            cultural_info="Sikku kolams are Tamil patterns symbolizing continuity, infinity, and protection."
        )
    return "Invalid file type", 400


@app.route("/generate", methods=["GET", "POST"])
def generate_pattern():
    if request.method == "POST":
        grid_size = int(request.form.get("grid_size", 5))
        symmetry = request.form.get("symmetry", "vertical")

        svg_content = svg_generator.create_svg(grid_size, symmetry)

        file_id = str(uuid.uuid4())[:8]
        svg_path = os.path.join(app.config["GENERATED_FOLDER"], f"pattern_{file_id}.svg")
        with open(svg_path, "w") as f:
            f.write(svg_content)

        return render_template(
            "generate.html",
            generated_svg=url_for("static", filename=f"generated/pattern_{file_id}.svg"),
            parameters={"grid_size": grid_size, "symmetry": symmetry}
        )
    return render_template("generate.html", generated_svg=None, parameters=None)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
