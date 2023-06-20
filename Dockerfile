FROM python:3.11-slim-buster

COPY . .
EXPOSE 5000
RUN ["python3", "-m", "pip", "install", "--upgrade", "pip"]
RUN ["python3", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

ENTRYPOINT ["./entrypoint.sh"]
RUN chmod u+x ./entrypoint.sh

CMD ["gunicorn app:app"]