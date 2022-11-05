FROM python:3.10.8-buster

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app
WORKDIR /usr/src/app

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "Server.main:app", "--port", "8000", "--host", "0.0.0.0", "--reload" ]
