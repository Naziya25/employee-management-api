\# Employee Management REST API



A REST API built using Python and FastAPI to manage employee records, integrated with SQLite and containerized using Docker.



\## Tech Stack



\- Python 3.12

\- FastAPI

\- SQLite

\- Docker

\- Docker Compose

\- Docker Hub



\## Features



\- Create and manage employee records

\- Retrieve employee information

\- Update employee details

\- Delete employee records

\- SQLite database integration

\- Docker containerization

\- Persistent storage using Docker volumes



\## Project Structure



```text

employee\_api/

├── main.py

├── database.py

├── requirements.txt

├── Dockerfile

├── compose.yaml

├── .dockerignore

├── .gitignore

└── README.md

```



\## Run Locally



Install dependencies:



```bash

pip install -r requirements.txt

```



Start the API:



```bash

uvicorn main:app --reload

```



Open Swagger documentation:



http://localhost:8000/docs



\## Run Using Docker



Build the image:



```bash

docker build -t employee-api .

```



Run the container:



```bash

docker run -d -p 8000:8000 --name employee-api-container employee-api

```



\## Docker Hub



Published Docker image:



`docker pull naziyanaz/employee-api:v1`



Replace the space in the command above with your Docker Hub repository username (`naziyanaz`):



```bash

docker pull naziyanaz/employee-api:v1

```



\## Learning Outcomes



\- REST API development using FastAPI

\- Docker images and containers

\- Dockerfile creation

\- Docker Compose

\- Docker volumes and bind mounts

\- Container networking

\- Docker image layers and build caching

\- Docker Hub image publishing

\- Git and GitHub version control



\## Author



Naziya



FDE Learning Journey | Backend Engineering | AI Engineering

