# flaskdockerized

A dockerized app built on top of Flask, and SQLAlchemy in Python3
It will create he schema when the server starts. I have also added 
an endpoint to seed the database.

### APIs endpoints:
##### [GET]
- > http://127.0.0.1:5000/api/documents/failed_extraction/customerId
- > http://127.0.0.1:5000/api/documents/failed_ingestion_count/customerId
- > http://127.0.0.1:5000/api/documents/summery/customerId
##### [POST]
- > http://127.0.0.1:5000/api/documents/seed 

## Steps to run
- Clone the repository
### using local:
- Setup .env file
- > python ./app/app.py
### using dockers:
- > docker-compose up
## Requirements

- Docker
- Docker Compose

## .ENV Example

DB_USERNAME=root

DB_PASSWORD=root

DB_HOST=localhost

DB_NAME=docs_db
