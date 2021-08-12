# Workout Tracker API

## Purpose
Purpose of this project is to create an API that allows for workout tracking/keeping a log of workouts categorized in different routines, primarily using Python Flask.

## Stages 
This project will attempt to go through multiple stages. 
1. The first goal is to have this project running successfully on a local environment(Database, API routes).
2. Once API is running successfully, build tests to test the different API routes, as well as individual functions
3. Next is to integrate Docker and create a container for this project.
4. Host this project on AWS and have it publicly accessible?. 
5. Use Jenkins to create a CI/CD pipeline () that will allow for code that is pushed to the repo, to be tested, and if tests are successful push code to a production environment.

## Technology
- Python
- Python Flask
- PostgreSQL (Maybe Google Sheets)
- Jenkins
- AWS

## How to run
1. Add a .env file to the root of the directory with the following contents
    ```
    DEBUG=True
    FLASK_ENV=development
    FLASK_APP=api
    ```
2. Now in the terminal enter:
    ```
    $ flask run
    ```
