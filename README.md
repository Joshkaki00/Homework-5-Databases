# Homework 5: Databases

## Table of Contents
1. [Overview](#overview)
2. [Setup](#setup)
3. [Running the Application](#running-the-application)
4. [Dependencies](#dependencies)
5. [License](#license)

## Overview

This project is a Flask web application that interacts with a MongoDB database to manage a collection of plants and their harvests. The application allows users to create, read, update, and delete plant records, as well as log harvests for each plant.

## Setup

1. **Clone the repository:**
    ```bash
    git clone /Users/joshkaki/ACS-1710-Web-Architecture-master/ACS-1710-Homework-5-Databases-Starter-master
    cd ACS-1710-Homework-5-Databases-Starter-master
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

## Running the Application

To run the application, execute the following command:
```bash
python app.py
```

The application will be available at `http://localhost:3000`.

## Dependencies

- Flask
- Flask-PyMongo
- bson

## License

This project is licensed under the MIT License.