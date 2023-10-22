format:
    black .

lint:
    ruff . --fix

lint-static:
    pyright

test:
    pytest tests -rP  # show tests with print