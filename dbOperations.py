import psycopg2
import random
from db_config import DATABASE_NAME, PASSWORD, USER, HOST
MAX_INT = (2**63)-1

def getConnection():
    return psycopg2.connect(dbname=DATABASE_NAME, user=USER, host=HOST, password=PASSWORD)

def execute(command):
    con = getConnection()
    cur = con.cursor()
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()


def execute_with_cursor(command, cursor):
    cursor.execute(command)

def create_record(table_name,field_name, field_value):
    command = f'INSERT INTO {table_name} ({field_name}) VALUES ({field_value})'
    execute(command)

def generate_unique_field(table_name, field_name):
    potential_id = -1
    con = getConnection()
    cur = con.cursor()

    while potential_id < 0 or len(select("*", table_name, f"{field_name}={str(potential_id)}")) > 0:
            potential_id = random.randint(0, MAX_INT)
    con.commit()
    cur.close()
    con.close()
    return potential_id

def select(SELECT, FROM, WHERE):
    con = getConnection()
    cur = con.cursor()
    execute_with_cursor(f'SELECT {SELECT} FROM {FROM} WHERE {WHERE};', cur)
    ret = cur.fetchall()
    cur.close()
    con.close()
    return ret

def get_inner_join_expression(table1, table2, on):
    return f"{table1} INNER JOIN {table2} ON {on}"

def get_and_expression(*statements):
    output = ""
    for index in range(0, len(statements)):
        if index > 0:
            output += " AND "
        output += statements[index]
    return output