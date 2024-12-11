# MLflow Deployment with Docker

This repository provides a Dockerized setup for **MLflow**, an open-source platform for managing the lifecycle of machine learning projects. The setup includes a **PostgreSQL** database as the backend store and **MinIO** for artifact storage.

---

## Features

- **MLflow Tracking Server**: Centralized platform for managing ML experiments.
- **PostgreSQL Backend**: Reliable metadata storage.
- **MinIO**: S3-compatible artifact storage.
- **Scalable Architecture**: Ready for production use.
- **Bucket Setup Automation**: Automatically creates required MinIO buckets.

---

## Prerequisites

1. Install Docker and Docker Compose:
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. Clone this repository:
   ```bash
   git clone https://github.com/Firas-Ruine/mlflow-docker-stack.git
   cd mlflow
   ```

3. Create an `.env` file in the root directory with the following content:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=mlflow
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_ACCESS_KEY=minioadmin
   ```

---

## Directory Structure

```
mlflow/
├── docker-compose.yml       # Defines services for MLflow, PostgreSQL, and MinIO
├── .env                     # Environment variables
├── postgres/
│   └── init.sql             # SQL initialization script for PostgreSQL
├── minio/
│   └── create-bucket.sh     # Script for creating required MinIO buckets
├── mlflow/
│   └── Dockerfile           # MLflow server custom build (optional)
└── README.md                # Documentation
```

---

## Getting Started

### Step 1: Build and Start the Containers
Run the following commands to build and start the services:

```bash
docker-compose build
docker-compose up -d
```

### Step 2: Verify Services
- **MLflow Tracking UI**: [http://localhost:5000](http://localhost:5000)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001)
  - Username: `minioadmin`
  - Password: `minioadmin`

---

## Configuration

### Environment Variables
The `.env` file allows you to configure key settings:
- **PostgreSQL**:
  - `POSTGRES_USER`: Username for the database.
  - `POSTGRES_PASSWORD`: Password for the database.
  - `POSTGRES_DB`: Database name.
- **MinIO**:
  - `MINIO_ACCESS_KEY`: Access key for MinIO.
  - `MINIO_SECRET_ACCESS_KEY`: Secret key for MinIO.

### Bucket Creation
The `create-bucket.sh` script automatically creates the required bucket (`mlflow`) for storing artifacts.

---

## Logging Experiments

Here’s an example of how to log experiments with this setup:

```python
import mlflow

# Set the MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:5001")

# Example experiment
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
```

Artifacts will be stored in MinIO under the `mlflow` bucket.

---

## Stopping and Cleaning Up

To stop the containers:
```bash
docker-compose down
```

To remove all containers, networks, and volumes:
```bash
docker-compose down -v
```

---

## Troubleshooting

### Common Issues
- **Database connection errors**: Ensure the `POSTGRES_PASSWORD` in `.env` matches the `--backend-store-uri` in `docker-compose.yml`.
- **Artifacts not found**: Verify that the `mlflow` bucket exists in MinIO.

### Logs
To view service logs:
```bash
docker-compose logs <service_name>
```

---

## Acknowledgments

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Docker Documentation](https://docs.docker.com/)
- [MinIO Documentation](https://docs.min.io/)
