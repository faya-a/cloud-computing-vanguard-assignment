.PHONY: setup install collectstatic developmentsuperuser

setup:
	python manage.py makemigrations storage
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input

install:
	pip install -r requirements.txt


developmentsuperuser:
	python manage.py createsuperuser --username developer \
	 --email developer@localhost.domain --noinput

runserver:
	python manage.py runserver


runserver-uwsgi:
	uwsgi --http=0.0.0.0:8080 -w cloudstorage.wsgi:application --static-map /static=files/static --static-map=/media=files/media
