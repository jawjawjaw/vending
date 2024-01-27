# Makefile for FastAPI project with Poetry and Docker Compose

# Define variables
APP_NAME = vending
DB_CONTAINER = my_fastapi_db



install-requirements: 
	@echo "Installing project requirements with Poetry..."
	poetry install
	@echo "Requirements installed."

generate-requirements:
	@echo "Generating a requirements.txt file..."
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	@echo "requirements.txt file generated."

# Database-related commands
create-migration:
	@echo "Creating a new Alembic migration..."
	poetry run alembic revision --autogenerate -m "$(msg)"
	@echo "Migration created."

run-migration:
	@echo "Running Alembic migrations..."
	poetry run alembic upgrade head
	@echo "Migrations executed."

# Application-related commands
run-app:
	@echo "Running the FastAPI application..."
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
	@echo "FastAPI application is running."

test:
	poetry run pytest

clean-db:
	@echo "Resetting database..."
	rm -rfd database_data
	@echo "Database reset."


lint:
	poetry run flake8 --ignore=E501,F401,F841,W503,E203 app 
	poetry run black  app
	poetry run isort app 
# Help target
help:
	@echo "Available targets:"
	@echo "  - install-requirements: Install project requirements with Poetry."
	@echo "  - generate-requirements: Generate a requirements.txt file from Poetry."
	@echo "  - create-migration msg={msg}: Create a new Alembic migration."
	@echo "  - run-migration: Run Alembic migrations."
	@echo "  - run-app: Run the FastAPI application."
	@echo "  - test: Run tests."
	@echo "  - clean-db: Reset local database."
	@echo "  - lint: Run linters." 

