from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "Thilak",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["Data Engineering", "ETL"],
) as dag:

    ingestion = BashOperator(
        task_id="Ingestion",
        bash_command="python /opt/airflow/pipeline/ingestion.py",
    )

    validation = BashOperator(
        task_id="Validation",
        bash_command="python /opt/airflow/pipeline/validation.py",
    )

    silver = BashOperator(
        task_id="Silver",
        bash_command="python /opt/airflow/pipeline/silver.py",
    )

    transformation = BashOperator(
        task_id="Transformation",
        bash_command="python /opt/airflow/pipeline/transformation.py",
    )

    scd_type_1 = BashOperator(
        task_id="SCD_Type_1",
        bash_command="python /opt/airflow/pipeline/scd_type_1.py",
    )

    scd_type_2 = BashOperator(
        task_id="SCD_Type_2",
        bash_command="python /opt/airflow/pipeline/scd_type_2.py",
    )

    gold = BashOperator(
        task_id="Gold",
        bash_command="python /opt/airflow/pipeline/gold.py",
    )

    load_to_postgres = BashOperator(
        task_id="Load_to_PostgreSQL",
        bash_command="python /opt/airflow/pipeline/load_to_postgres.py",
    )

    metadata = BashOperator(
        task_id="Metadata",
        bash_command="python /opt/airflow/pipeline/metadata.py",
    )

    audit = BashOperator(
        task_id="Audit",
        bash_command="python /opt/airflow/pipeline/audit.py",
    )

    (
        ingestion
        >> validation
        >> silver
        >> transformation
        >> scd_type_1
        >> scd_type_2
        >> gold
        >> load_to_postgres
        >> metadata
        >> audit
    )