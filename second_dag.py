from airflow.sdk import dag, task
from datetime import datetime

from tornado.process import task_id


@dag(dag_id="my_dag", schedule="* * * * *", start_date=datetime(2025, 1, 1))
def my_dag():

    @task
    def my_task():
        print("my task 1")
        return 1

    @task
    def my_task2():
        print("my task 2")
        return 2

    @task
    def my_task3():
        print("my task 3")
        return 3

    my_task()
    my_task2()
    my_task3()

my_dag()
