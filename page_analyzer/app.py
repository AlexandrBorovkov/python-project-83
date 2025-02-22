import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.parse import seo_analysis, url_parse
from page_analyzer.repository import UrlRepository
from page_analyzer.validator import validate

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DATABASE_URL'] = os.getenv("DATABASE_URL")

repo = UrlRepository(app.config['DATABASE_URL'])


@app.route("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post("/urls")
def posts_url():
    data = request.form.to_dict()
    if validate(data):
        data["url"] = url_parse(data["url"])
        url = repo.find_by_name(data["url"])
        if url:
            flash("Страница уже существует", "info")
            return redirect(url_for("get_url", id=url["id"]))
        repo.save_url(data)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("get_url", id=data["id"]))
    else:
        flash("Некорректный URL", "danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422


@app.route("/urls")
def get_urls():
    urls = repo.get_content()
    return render_template("urls.html", urls=urls)


@app.route("/urls/<id>")
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find_by_id(id)
    if url is None:
        return 'Page not found', 404
    url_checks = repo.get_checks(id)
    return render_template(
        'show.html',
        url=url,
        url_checks=url_checks,
        messages=messages
        )


@app.post("/urls/<id>/checks")
def check_url(id):
    url = repo.find_by_id(id)
    data = seo_analysis(url["name"])
    if data:
        data["url_id"] = id
        repo.save_check(data)
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for('get_url', id=id))
