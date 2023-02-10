setup_local:
	python3 -m venv venv && python3 -m pip install -r functions/requirements.txt

setup_test_local:
	python3 -m venv venv && python3 -m pip install -r tests/requirements.txt

build:
	sam build --skip-pull-image

build_and_deploy_dev:
	make build
	sam deploy --config-env dev

run_unit_tests:
	python -m pytest tests/unit -v

run_unit_tests_with_echo:
	python -m pytest tests/unit -v --capture=no

run_integration_tests:
	python -m pytest tests/integration -v

run_integration_tests_with_echo:
	python -m pytest tests/integration -v --capture=no

clear_cache:
	find . -type d -name __pycache__ -exec rm -r {} \+
	rm -rf .pytest_cache .aws-sam