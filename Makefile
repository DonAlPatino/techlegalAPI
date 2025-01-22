python = venv/Scripts/python
pip = venv/Scripts/pip

all: build down up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

venv:
	venv\Scripts\activate.bat

setup:
	python -m venv venv
	$(python) -m pip install --upgrade pip
	$(pip) install -r requirements.txt

run:
	$(python) main.py

test:
	$(python) -m pytest

clean:
	@if exist steps\__pycache__ (rmdir /s /q steps\__pycache__)
	@if exist __pycache__ (rmdir /s /q __pycache__)
	@if exist .pytest_cache (rmdir /s /q .pytest_cache)
	@if exist tests\__pycache__ (rmdir /s /q tests\__pycache__)

remove:
	@if exist venv (rmdir /s /q venv)