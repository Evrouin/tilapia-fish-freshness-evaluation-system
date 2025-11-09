.PHONY: help install install-dev format lint type-check test clean run

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

format:  ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

lint:  ## Run flake8 linter
	flake8 src/ tests/ --extend-ignore=E203,W503,E501

type-check:  ## Run mypy type checker
	mypy src/

test:  ## Run tests with pytest
	pytest tests/ -v --cov=src/tilapia_freshness

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run:  ## Run the application
	python main.py

check-all: format lint type-check test  ## Run all quality checks
