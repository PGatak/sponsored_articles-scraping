.PHONY: all scraping web clean

DBNAME		?= artsql


all:

scraping:
	PYTHONPATH=. python scraping/scraping.py

web:
	PYTHONPATH=. python web/web.py

clean:
	find . -type d -name __pycache__ | xargs rm -rfv

initdb:
	dropdb --if-exists $(DBNAME)
	createdb $(DBNAME)
	psql -1 $(DBNAME) < sql/schema.sql
