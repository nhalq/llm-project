FROM python:3.10.14-slim
RUN apt-get -y update

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["fastapi", "run", "main.py"]

