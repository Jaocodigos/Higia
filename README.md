# Higia
The prototype of a helpfull hospital system.

### Required resources

- Python 3.11

## How run the project

### Create a virtual environment(venv) and activate it.

```bash
    python -m venv /path/to/new/virtual/environment
    .venv\Scripts\activate # For windows
    .venv/bin/activate # For linux distros
```

### Install requirements

```bash
    pip install -r docker/engine/requirements.txt
```

### Fill required envs:

- ADMIN_USERNAME 
- ADMIN_PASSWORD
- SECRET_KEY
- FLASK_APP=engine:application
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DATABASE
- MYSQL_HOST

**OBS:** Maybe you need to define the project structure to run it correctly. In this case, you must set the **docker** folder as the root directory.

### Running migrations

```bash
    flask db upgrade
```

### Running Higia

```bash
    flask run -h 0.0.0.0 -p your_port
```


