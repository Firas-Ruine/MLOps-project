FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean
RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install DVC
RUN pip install dvc[all]

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
