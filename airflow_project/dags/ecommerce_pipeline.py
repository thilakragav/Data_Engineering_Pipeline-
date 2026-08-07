from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "Thilak",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="End-to-End Ecommerce Data Engineering Pipeline",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["ETL", "Medallion", "Data Engineering"],
) as dag:

    # =====================================================
    # Ingestion
    # =====================================================

    ingestion = BashOperator(
        task_id="ingestion",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.run_ingestion
        """,
    )

    # =====================================================
    # Staging
    # =====================================================

    staging = BashOperator(
        task_id="staging",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.staging
        """,
    )

    # =====================================================
    # Bronze
    # =====================================================

    bronze = BashOperator(
        task_id="bronze",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.bronze
        """,
    )

    # =====================================================
    # Validation
    # =====================================================

    validation = BashOperator(
        task_id="validation",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.validation
        """,
    )

    # =====================================================
    # Silver
    # =====================================================

    silver = BashOperator(
        task_id="silver",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.silver
        """,
    )

    # =====================================================
    # Transformation
    # =====================================================

    transformation = BashOperator(
        task_id="transformation",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.transformation
        """,
    )

    # =====================================================
    # SCD Type 1
    # =====================================================

    scd_type_1 = BashOperator(
        task_id="scd_type_1",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.scd_type_1
        """,
    )

    # =====================================================
    # SCD Type 2
    # =====================================================

    scd_type_2 = BashOperator(
        task_id="scd_type_2",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.scd_type_2
        """,
    )

    # =====================================================
    # Gold
    # =====================================================

    gold = BashOperator(
        task_id="gold",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.gold
        """,
    )

    # =====================================================
    # PostgreSQL
    # =====================================================

    load_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.load_to_postgres
        """,
    )

    # =====================================================
    # Metadata
    # =====================================================

    metadata = BashOperator(
        task_id="metadata",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.metadata
        """,
    )

    # =====================================================
    # Audit
    # =====================================================

    audit = BashOperator(
        task_id="audit",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.audit
        """,
    )

    # =====================================================
    # Email Notification
    # =====================================================

    send_email = BashOperator(
        task_id="send_email",
        bash_command="""
        cd /opt/airflow &&
        python -m pipeline.send_email
        """,
    )

    (
        ingestion
        >> staging
        >> bronze
        >> validation
        >> silver
        >> transformation
        >> scd_type_1
        >> scd_type_2
        >> gold
        >> load_postgres
        >> metadata
        >> audit
        >> send_email
    )