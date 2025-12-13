.PHONY: dev test lint format check

dev:
	uv run fastapi dev app/main.py --port 8080

test:
	uv run pytest

check_migrations:
	uv run alembic check

manual_migration:
	@test -n "$(msg)" || (echo "ERROR: msg is required"; exit 1)
	uv run alembic revision -m "$(msg)"

auto_migration:
	@test -n "$(msg)" || (echo "ERROR: msg is required"; exit 1)
	uv run alembic revision --autogenerate -m "$(msg)"

run_migrations:
	uv run alembic upgrade head
