check_formatting:
	@echo "Checking formatting..."
	black ./src ./tests --check
	flake8 ./src ./tests

db_migration:
	@echo "Creating migration..."
	cd migrations && alembic upgrade head

create_test_environment:
	@echo "Creating test environment..."
	docker-compose -f docker-compose.test.yml up -d

unittest:
	@echo "Running unittests..."
	 python3 -m pytest tests/unit


e2e:
	@echo "Running unittests..."
	 python3 -m pytest tests/e2e


docker_start:
	@echo "Starting docker containers..."
	docker-compose -f docker-compose.test.yml up -d --build


docker_stop:
	@echo "Stopping docker containers..."
	docker-compose -f docker-compose.test.yml down
