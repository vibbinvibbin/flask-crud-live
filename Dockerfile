FROM python:3.12.7-alpine

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /app

COPY requirements.txt ./


RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]