FROM python:3.11-slim-buster

COPY . .
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
RUN chmod u+x ./entrypoint.sh

RUN ["python3", "-m", "flask", "db", "init"]
RUN ["python3", "-m", "flask", "db", "upgrade"]

CMD ["gunicorn app:app"]