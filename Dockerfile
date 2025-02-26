FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install boto3 pymysql

CMD ["python", "app.py"]
