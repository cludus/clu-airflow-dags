from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id='simple_sequential_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    task1 = BashOperator(
        task_id='start_task',
        bash_command='echo "Starting workflow"',
    )

    task2 = BashOperator(
        task_id='middle_task',
        bash_command='echo "Processing data"',
    )

    task3 = BashOperator(
        task_id='end_task',
        bash_command='echo "Workflow finished"',
    )

    task1 >> task2 >> task3