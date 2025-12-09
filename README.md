# REST API with Fast API with TDD
This app demonstrates how to do test driven development with Python using Fast API to build a REST API app

## Features
This app provides functionalities such as:

- Home [GET]: Retrieve application status with a welcome message
- Register [POST]: Create a user on the REST API app
- View [GET]: Retrieve user details such as `id` `name`, `email`, `phone`, `username`, `password`, `location`, `creation_date`, `last_login_date` and `last_modified_date`
- Login [POST]: Authenticate a registered user
- Update [PUT]: Update user's details such as `name`, `email`, `phone`, `username`, `password`, `location`

## Running
To start the app on localhost, clone the code and create a virtual environment, install the requirements listed on `requirements.txt` then use the command below to run the app
```commandline
uvicorn app.rest_api_app:app --reload 
```

## Testing
First, make sure that the app is running on localhost. Run tests with the command below. See screenshot attached below for details
```commandline
python -m unittest tests.test_rest_api_app
```

![Tests](https://github.com/murageden/simple-tdd-calculator-app/blob/main/Screenshot%202025-12-05%20074727.png?raw=true "Tests")