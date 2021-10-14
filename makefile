all: list-targets

.PHONY: all list-targets venv
list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]'

run:
	@. venv/bin/activate && \
		python bot.py && \
		deactivate

scrape:
	@. venv/bin/activate && \
		python scraper.py && \
		deactivate

setup: venv dep

venv:
	@python3 -m venv ./venv/

dep:
	@. venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

version:
	@. venv/bin/activate && \
		python --version && \
		deactivate
