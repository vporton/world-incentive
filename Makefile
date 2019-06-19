#!/usr/bin/make -f

.PHONY: all
all: fixtures

.PHONY: fixtures
fixtures:
	./manage.py loaddata initiative/fixtures/categories.json

.PHONY: update
update:
	./manage.py cities --import country,region,subregion,city,district
