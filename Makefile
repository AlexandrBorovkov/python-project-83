PORT ?= 8000

install:
	uv sync

build:
	./build.sh

lint:
	uv run ruff check

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
