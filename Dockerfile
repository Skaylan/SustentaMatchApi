FROM python:3.11-slim-buster

COPY . .
EXPOSE 5000
ENTRYPOINT ["python"]

RUN ["python3", "-m", "pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

RUN ["python3", "-m", "flask", "db", "init"]
RUN ["python3", "-m", "flask", "db", "upgrade"]


CMD ["gunicorn app:app"]