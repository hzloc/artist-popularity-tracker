import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from src.db_store.store import Store
from src.pipeline.run import Pipeline
from src.providers.base import Provider
from src.providers.lastfm import LastFm
from src.providers.soundcharts import SoundCharts
from src.utils.logger import get_logger

load_dotenv()

default_args = {
    "depends_on_past": False,
    "start_date": datetime.now(),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

def create_dag_for(provider: Provider, dag_name: str, schedule: str = "0 0 * * *"):
    dag = DAG(dag_id=dag_name, default_args=default_args, schedule=schedule)
    store = Store()
    pipeline = Pipeline(provider=provider, store=store)

    with dag:
        start_task = EmptyOperator(task_id="start_task")
        run_pipeline = PythonOperator(task_id="run_pipeline", python_callable=pipeline.run, params={})

    start_task >> run_pipeline

    return dag

log = get_logger("DAG", level=logging.INFO)
lastfm = LastFm(log)
soundcharts = SoundCharts(log)

create_dag_for(lastfm, dag_name="lastfm")
create_dag_for(soundcharts, dag_name="soundcharts")
