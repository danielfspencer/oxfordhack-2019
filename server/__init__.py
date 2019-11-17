import random
import string
import os
import zipfile
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from . import creator

app = Flask(__name__)

UPLOADS = "/tmp/uploads/"
os.makedirs(UPLOADS, exist_ok=True)


@app.route("/")
@app.route("/<name>")
def index(name=None):
    return render_template("index.html", name=name)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        if "album" not in request.files:
            return redirect(request.url)
        album = request.files["album"]

        if not album.filename:
            return redirect(request.url)

        if album.filename.split(".", 1)[1] != "zip":
            return redirect(request.url)

        filename = secure_filename(album.filename)
        location = os.path.join(UPLOADS, filename)
        album.save(location)

        with zipfile.ZipFile(location, "r") as z:
            extraction_location = os.path.join(UPLOADS, random_id(12))
            os.mkdir(extraction_location)
            z.extractall(extraction_location)

        creator.create(extraction_location)

        return render_template("font-preview.html")
    else:
        return render_template("index.html")


def random_id(n):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(n))
