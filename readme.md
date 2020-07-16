# README.MD

Hangman is a popular game played by millions across the world. This repository contains my attempt to recreate it within Python.

## Installation
Best practice is to create a Python3 virtual environment and then install the dependencies in the requirements.txt file via Pip.

```bash
virtualenv -p python3 venv
pip install -r requirements.txt
```

## Configuration
In order for the application to run properly and connect to the word generator API, an API key should be created on [RapidAPI](https://rapidapi.com/). This API key should then be saved as an environment variables with the name 'RAPID_API_KEY'.

Sadly, the external api seems to suffer a lot of downtime. To combat this, the application includes a config.json file from which words will be loaded whenever the api is unavailable.