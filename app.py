from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from models import db, Notes


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/notes", methods=["GET", "POST"])
def notes_page():

    if request.method == "POST":

        title = request.form["title"]
        text = request.form["text"]

        new_note = Notes(
            title=title,
            text=text
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("notes_page"))

    notes = Notes.query.all()

    return render_template(
        "notes.html",
        notes=notes
    )


if __name__ == "__main__":
    app.run(debug=True)