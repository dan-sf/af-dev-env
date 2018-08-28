"""
This is some example code that can be used to query Airflow's backing db from
the Airflow instances (using only Airflow dependencies). Another way to
interact with the Airflow db would be to log into the Postgres instance and run
'psql airflow airflow', this will activate a SQL REPL where queries can be
executed. For Airflow 1.9.0 and older you need to interact with the backing db
to clean up old dags that are no longer used.
"""
import os
import psycopg2

target_dag = 'DAG-NAME'
tables = ['xcom', 'task_instance', 'sla_miss', 'log', 'job', 'dag_run', 'dag']

conn_dict = {
    'host': 'postgres',
    'user': 'airflow',
    'port': '5432',
    'dbname': 'airflow',
    'password': 'airflow',
}

conn = psycopg2.connect(**conn_dict)
cur = conn.cursor()

# Testing cursor/connection
cur.execute("select * from dag limit 10;")
dag_records = cur.fetchall()

# Remove a dag
for table in tables:
    sql = "delete from {} where dag_id='{}'".format(table, target_dag)
    cur.execute(sql)

# Check if the dag has actually been fully removed
for table in tables:
    sql = "select * from {} where dag_id='{}'".format(table, target_dag)
    cur.execute(sql)
    f = cur.fetchall()
    if f != []:
        print(table, f)

# Changes to the backing db aren't final until we commit them
conn.commit()

# Close up cursor and connection to the db
cur.close()
conn.close()

