dev:
	pipenv run python workflow.py

format:
	pipenv run black .

lint:
	pipenv run pylint .

type:
	pipenv run mypy .
