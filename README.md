# FASTAPI

## How to setup project?

### Clone the project from Gitlab using HTTPS

```sh
git https://github.com/pratiksha205/FASTAPI.git
cd backend
```

## activate virtual environment
```sh
$ source venv/bin/activate
```
## freeze requirement.txt
$ pip freeze > requirements. txt

## Then install the dependencies

(venv)$ pip install -r requirements.txt

## Run the server
(venv)$ cd backend
(venv)$ uvicorn main:app --reload