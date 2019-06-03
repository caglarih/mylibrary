build:
	docker-compose build
up:
	docker-compose up -d
bash:
	docker-compose exec django bash
shell:
	docker-compose exec django pyhton manage.py shell
restart:
	docker-compose restart
log:
	docker-compose logs -f django
celerylog:
	docker-compose logs -f celery
makemigrations:
	docker-compose run -rm django python manage.py makemigrations
migrate:
	docker-compose run -rm django python manage.py migrate
removedb:
	docker volume rm mylibrary_postgres_data
