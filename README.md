# flask4-html

APP.PY


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



INDEX.HTML


<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{% block title %}Мой блог{% endblock %}</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>

    <header>
        <h1>Мой блог программиста</h1>

        <nav>
            <a href="/">Главная</a>
            <a href="/notes">Дневник программиста</a>
        </nav>
    </header>

    <main>
        {% block content %}

        <h2>Добро пожаловать!</h2>

        <p>
            Это мой учебный блог по программированию.
        </p>

        {% endblock %}
    </main>

    <footer>
        <p>Учебный проект Flask + Jinja2</p>
    </footer>

</body>
</html>



NOTES.HTML


{% extends "index.html" %}

{% block title %}
Дневник программиста
{% endblock %}

{% block content %}

<h2>Дневник программиста</h2>

<section class="form-section">

    <h3>Добавить новую запись</h3>

    <form method="POST">

        <label for="title">Заголовок записи:</label>

        <input
            type="text"
            id="title"
            name="title"
            required
        >

        <label for="text">Текст записи:</label>

        <textarea
            id="text"
            name="text"
            rows="6"
            required
        ></textarea>

        <button type="submit">
            Добавить запись
        </button>

    </form>

</section>


<section class="notes-section">

    <h3>Мои записи</h3>

    {% if notes %}

        {% for note in notes %}

            <article class="note">

                <h3>{{ note.title }}</h3>

                <p>{{ note.text }}</p>

            </article>

        {% endfor %}

    {% else %}

        <p>Пока нет ни одной записи.</p>

    {% endif %}

</section>

{% endblock %}



STYLE.CSS


* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #f2f2f2;
    color: #333;
}

header {
    background-color: #222;
    color: white;
    padding: 25px;
    text-align: center;
}

header h1 {
    margin: 0 0 20px;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
}

nav a:hover {
    text-decoration: underline;
}

main {
    max-width: 900px;
    margin: 30px auto;
    padding: 30px;
    background-color: white;
    border-radius: 10px;
}

h2 {
    color: #333;
}

.form-section {
    margin-bottom: 40px;
}

form {
    display: flex;
    flex-direction: column;
}

label {
    margin-top: 15px;
    margin-bottom: 5px;
    font-weight: bold;
}

input,
textarea {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
}

button {
    margin-top: 20px;
    padding: 12px;
    border: none;
    border-radius: 5px;
    background-color: #333;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background-color: #555;
}

.note {
    margin-top: 20px;
    padding: 20px;
    background-color: #f5f5f5;
    border-left: 5px solid #333;
    border-radius: 5px;
}

.note h3 {
    margin-top: 0;
}

footer {
    text-align: center;
    padding: 20px;
    color: #777;
}


MODELS.PY


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
