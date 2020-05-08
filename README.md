# Running the Program
By default, the frontend communicates with the ec2 server.
If this needs to be changed, comment/uncomment the corresponding lines in ```.../group_01/frontend/pyarcade/connection.py``` on line numbers 6 and 7

## Build Instructions
1. ```$ .../group_01/```
1. ```docker-compose build```
1. ```docker-compose up -d```

## Running the UI
1. ```docker exec -it pyarcade_frontend python pyarcade/start.py```

## Stopping
1. ```docker-compose down```

# Users
login: alice
passw: password

login: bob
passw: password

login: eve
passw: password


## Run Tests
### Frontend
1. ```$ .../group_01/frontend/```
2. ```coverage run setup.py test```
3. ```coverage report -m```

### Backend
(**```pip install django``` may be need**)
1. ```$ .../group_01/backend/```
2. ```python manage.py test pyarcade_backend```

# Work
## Sprint 1
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

## Sprint 2
- Andy - 25%
    - Horseman UI
    - UI signup/login
    - Different game difficulty UI

- Brandon - 25%
    - User status backend code
    - Games played backend code
    - Game difficulties for mastermind

- Nam - 25%
    - JWT authentication for users
    - Game model and tests for backend
    - Reset statistics backend code

- Ryan - 25%
    - Horseman game logic
    - Games won stats backend code

## Sprint 3
- Andy - 25%
    - Leaderboard UI
    - Account/Friends list UI
    - Instructions UI

- Brandon - 25%
    - Setup EC2 server
    - Sphinx Documentation

- Nam - 25%
    - Leaderboard backend code
    - CI/CD pipeline
    - Setup https for EC2 server

- Ryan - 25%
    - Setup EC2 Server
    - Friendship model 
    - Adding and retrieving friends backend code

