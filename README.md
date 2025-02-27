# Educational project "Page Analyzer" #

### Hexlet tests and linter status:
[![Actions Status](https://github.com/AlexandrBorovkov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AlexandrBorovkov/python-project-83/actions)
[![check_app](https://github.com/AlexandrBorovkov/python-project-83/actions/workflows/check_app.yml/badge.svg)](https://github.com/AlexandrBorovkov/python-project-83/actions/workflows/check_app.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bb373c7d77f76ff919f3/maintainability)](https://codeclimate.com/github/AlexandrBorovkov/python-project-83/maintainability)

---

### Links ###

#### [Link to the web application](https://python-project-83-ke72.onrender.com) ####

### This project was built using these tools: ###

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [python](https://www.python.org/downloads/)                                 | "Python is a programming language"      |
| [uv](https://docs.astral.sh/uv/)                                            | "Python dependency management and packaging made easy"|
| [flask](https://flask.palletsprojects.com/en/stable/)                       | "Flask is a lightweight WSGI web application framework" |
| [gunicorn](https://docs.gunicorn.org/en/latest/)                            | "Python WSGI HTTP Server for UNIX"|
| [psycopg2-binary](https://www.psycopg.org/docs/)                            | "PostgreSQL Database Adapter for Python programming language"|
| [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)    | "Python library for pulling data out of HTML and XML files"|
| [lxml](https://pypi.org/project/lxml/)                                      | "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API"|
| [requests](https://requests.readthedocs.io/en/latest/)                      | "Simple HTTP library for Python"|
| [python-dotenv](https://pypi.org/project/python-dotenv/)                    | "Python-dotenv reads key-value pairs from a .env file and can set them as environment variables"|
| [validators](https://validators.readthedocs.io/en/latest/)                  | "Python Data Validation"|
| [ruff](https://docs.astral.sh/ruff/)                                        | "Your tool for style guide enforcement"|

---

### Description: ###
"Page Analyzer is a website that analyzes the specified pages for SEO suitability"

---

### How do I launch the app? ###
1. **Clone the repository**:
   ```sh
   git clone https://github.com/AlexandrBorovkov/python-project-83.git
   cd python-project-83
   ```
2. **Set up environment variables (`.env`)**:
   ```sh
   DATABASE_URL=postgresql://user:password@localhost:5432/database
   SECRET_KEY=your_secret_key
   ```
3. **Installing dependencies and creating database tables**:
   ```sh
   make build
   make install
   ```
4. **Run the application**:
   - In **development** (Flask + Debug Mode):
     ```sh
     make dev
     ```
   - In **production** (Gunicorn + PostgreSQL):
     ```sh
     make start
     ```