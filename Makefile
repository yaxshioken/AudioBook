mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser --email test@gmail.com
sort:
	black .
	isort .
celery_worker:
	 celery -A config worker --loglevel=info