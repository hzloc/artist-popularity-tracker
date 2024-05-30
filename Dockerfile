FROM apache/airflow:2.9.1
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
