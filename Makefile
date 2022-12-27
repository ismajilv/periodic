check_formatting:
	@echo "Checking formatting..."
	black ./src ./tests --check
	flake8 ./src ./tests

install_dependencies:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

db_migration:
	@echo "Creating migration..."
	alembic -c ./migrations/alembic.ini upgrade head

create_test_environment:
	@echo "Creating test environment..."
	docker-compose -f docker-compose.test.yml up  --build -d


delete_test_environment:
	@echo "Deleting test environment..."
	docker-compose -f docker-compose.test.yml down


test_unittest:
	@echo "Running unittests..."
	 python3 -m pytest tests/unit


test_e2e:
	@echo "Running unittests..."
	 python3 -m pytest tests/e2e


test_integration:
	@echo "Running unittests..."
	 python3 -m pytest tests/e2e
