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

from page_analyzer.parse import seo_analysis
from page_analyzer.repository import UrlRepository
from page_analyzer.utils import normalize_url, validate_url

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
    url = request.form['url']
    error_msg = validate_url(url)
    if error_msg:
        flash(error_msg, "danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422
    normalized_url = normalize_url(url)
    existed_url = repo.find_by_name(normalized_url)
    if existed_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("get_url", id=existed_url["id"]))
    url_id = repo.save_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=url_id))


@app.route("/urls")
def get_urls():
    urls = repo.get_content()
    return render_template("urls.html", urls=urls)


@app.route("/urls/<int:id>")
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find_by_id(id)
    if url is None:
        return render_template('page404.html'), 404
    url_checks = repo.get_checks(id)
    return render_template(
        'show.html',
        url=url,
        url_checks=url_checks,
        messages=messages
        )


@app.post("/urls/<int:id>/checks")
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404
