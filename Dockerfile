FROM python:3.11-slim-buster

COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["py run.py"]