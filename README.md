## Steps to run this project

- Create a new python environment and install dependencies

```python
conda create --name elastic-search python=3.12
conda activate elastic-search
conda install pip
pip install -r requirements.txt
```
- Run docker compose

```python
docker-compose up -d
```

- Run alembic to create database table

```python
alembic upgrade head;
```

- Run app

```python
fastapi run src --reload
```

- Access APIs : head to `http://0.0.0.0:8000/docs`


#### Misc
- curl -X DELETE "localhost:9200/posts?pretty"
- alembic revision --autogenerate -m "update primary id field"





