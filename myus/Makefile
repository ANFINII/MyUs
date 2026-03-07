.PHONY: makers lint isort

# lint check + import sort
makers:
	@echo "Running import sort..."
	ruff check --fix --select I .
	@echo "Running mypy..."
	DJANGO_SETTINGS_MODULE=config.settings.local mypy api/

# mypyのみ
lint:
	DJANGO_SETTINGS_MODULE=config.settings.local mypy api/

# importソートのみ
isort:
	ruff check --fix --select I .
