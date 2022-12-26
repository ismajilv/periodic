check_formatting:
	@echo "Checking formatting..."
	black ./src --check
	flake8 ./src

db_migration:
	@echo "Creating migration..."
	cd migrations && alembic upgrade head

test_environment:
	@echo "Creating test environment..."
	docker-compose -f docker-compose.test.yml up -d
