build:
	docker-compose build

stop:
	docker-compose down

run:
	docker-compose up --build -d

logs:
	docker-compose logs -f

