## Synopsis

## How to Run (Development)

1. Create or re-initialize the database

2. Run the project locally
- % cd web
- % python run-dev.py
- % cd ..

Go to your favorite web browser and open:
    http://127.0.0.1:5000


3. Build and run the Docker containers (Not yet implemented)
- % docker-compose build
- % docker-compose up -d


## Key Python Modules Used

- Flask - web framework
- Jinga2 - templating engine
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - password hashing
- Flask-Login - support for user management
- Flask-Security
- Flask-WTF - simplifies forms
- Flask-MongoEngine

This application is written using Python 2.7.  The database used is MongoDB.

Docker is the recommended tool for running in development and production nut not yet available.

## Unit Testing


For running a specific module:
    % nose2 -v project.tests.test_recipes_api
