FROM python:3.10.14

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py"]

