import sqlite3
import os

import config


def get_db_connection(db):
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/..' + config.db_config[db]['url']
    return sqlite3.Connection(database=file_path)


def close_db_connection(conn):
    conn.close()


def fetch_data(query, db):
    conn = get_db_connection(db)
    cursor = conn.execute(query)

    data = [list(t) for t in cursor.fetchall()]
    column_names = get_column_names(cursor)
    conn.close()
    data.insert(0, column_names)
    return data


def execute_statement(statement, db):
    conn = get_db_connection(db)
    cursor = conn.execute(statement)
    conn.commit()
    conn.close()


def get_column_names(cursor):
    return list(map(lambda x: x[0], cursor.description))


def get_query_from_file(sql_path):
    with open(sql_path) as f:
        return f.read()


def convert_list_for_sql(list_params):
    l = [convert_params_for_sql(l) for l in list_params]
    return ', '.join(map(str, l))


def convert_strings_for_sql(s):
    return "\'" + s + "\'"


def convert_params_for_sql(v):
    if isinstance(v, str):
        return convert_strings_for_sql(v)
    elif isinstance(v, list):
        return convert_list_for_sql(v)
    else:
        return str(v)


def replace_param(sql, k, v):
    return sql.replace(f"@{k}", convert_params_for_sql(v))


def add_params_to_query(sql, params):
    for k, v in params.items():
        sql = replace_param(sql, k, v)
    return sql


def sql_query_from_file(sql_path, params):
    sql = get_query_from_file(sql_path)
    if params is None:
        return sql
    else:
        return add_params_to_query(sql, params)


def fetch_data_from_file(sql_path, db, params=None):
    sql = sql_query_from_file(sql_path, params)
    return fetch_data(db=db, query=sql)