import psycopg2
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.config import DATABASE_URL, SECRET_KEY
from page_analyzer.repository import UrlRepository
from page_analyzer.url_parse import url_parse
from page_analyzer.validator import validate

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

conn = psycopg2.connect(DATABASE_URL)
repo = UrlRepository(conn)

repo.create_table()


@app.route("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post("/urls")
def posts_url():

    data = request.form.to_dict()

    if validate(data):
        data["url"] = url_parse(data["url"])
        if repo.save(data):
            flash("Страница успешно добавлена", "success")
            return redirect(url_for("get_url", id=data["id"]))
        flash("Страница уже существует", "info")  # Нужно сменить цвет
        return redirect(url_for("index"))
    else:
        flash("Некорректный URL", "error")
        return redirect(url_for("index"))


@app.route("/urls")
def get_urls():
    urls = repo.get_content()
    return render_template("urls.html", urls=urls)


@app.route("/urls/<id>")
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id)
    if url is None:
        return 'Page not found', 404
    return render_template('show.html', url=url, messages=messages)
