FROM python:3.11-slim-buster

COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]

RUN chmod u+x ./entrypoint.sh
CMD ["gunicorn app:app"]