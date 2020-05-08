# Running the Program
## Build Instructions
1. ```$ .../group_01/```
1. ```docker-compose build```
1. ```docker-compose up -d```

## Running the UI
1. ```docker exec -it pyarcade_frontend python pyarcade/start.py```

## Stopping
1. ```docker-compose down```

## Run Tests
### Frontend
1. ```$ .../group_01/frontend/```
2. ```coverage run setup.py test```
3. ```coverage report -m```

### Backend
(**```pip install django``` may be need**)
1. ```$ .../group_01/backend/```
2. ```python manage.py test pyarcade_backend```

# Users
login: alice
passw: password

login: bob
passw: password

login: eve
passw: password


# Work
- Andy - 25%
    - War and Go Fish UI
    - Added new UI test
    - UI signup and connection

- Brandon - 25%
    - Refactored and integrated War
    - Refactored War tests

- Nam - 25%
    - django, nginx setup
    - Refactored Connect4 and corresponding tests
    - Docker setup

- Ryan - 25%
    - Refactored and integrated Go Fish
    - Refactored Go Fish tests


