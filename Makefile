APP_LIST ?= blog bookstore_project books pages users orders 
.PHONY: collectstatic run test ci install install-dev migrations staticfiles

help:
	@echo "Available commands"
	@echo " - ci               : lints, migrations, tests, coverage"
	@echo " - install          : installs production requirements"
	@echo " - install-dev      : installs development requirements"
	@echo " - isort            : sorts all imports of the project"
	@echo " - lint             : lints the codebase"
	@echo " - run              : runs the development server"
	@echo " - setup-test-data  : erases the db and loads mock data"
	@echo " - shellplus        : runs the development shell"

collectstatic:
	python manage.py collectstatic --noinput

clean:
	rm -rf __pycache__ .pytest_cache

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy

install:
	poetry install

update:
	poetry update
	
setup_test_data:
	python manage.py setup_test_data
	
shellplus:
	python manage.py shell_plus --print-sql

shell:
	python manage.py shell

showmigrations:
	python manage.py showmigrations

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

migrations-check:
	python manage.py makemigrations --check --dry-run

isort:
	poetry run isort . --check-only --profile black

format:
	poetry run black . --check 

lint: isort format
	poetry run flake8 .

test: check migrations-check
	coverage run manage.py test
	coverage html

security:
	poetry run bandit -r .
	poetry run safety check

ci: lint security test
	
reload:
	echo "Reloading daemon..."
	sudo systemctl daemon-reload
	echo "Reloading gunicorn..."
	sudo systemctl restart bookstore-gunicorn
	echo "Reloading scheduler..."
	sudo systemctl restart bookstore-scheduler
	echo "Reloading nginx..."
	sudo nginx -s reload
	echo "All done! 💅💫💖"