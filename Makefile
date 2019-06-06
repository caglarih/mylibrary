build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
bash:
	docker-compose run --rm django bash
shell:
	docker-compose run --rm django python manage.py shell
restart:
	docker-compose restart
log:
	docker-compose logs -f django
celerylog:
	docker-compose logs -f celery
makemigrations:
	docker-compose run --rm django python manage.py makemigrations
migrate:
	docker-compose run --rm django python manage.py migrate
test:
	docker-compose run --rm django nosetests tests
djtest:
	docker-compose run --rm django python manage.py test
removedb:
	docker volume rm mylibrary_postgres_data
