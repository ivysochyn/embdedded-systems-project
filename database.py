#!/usr/bin/python3

import sqlite3
from sqlite3 import Error

sql_create_attendance_table = """ CREATE TABLE IF NOT EXISTS attendance (
                                    name text NOT NULL,
                                    date text NOT NULL,
                                    time text NOT NULL
                                ); """


def create_connection(db_file):
    """
    Create a database connection to a SQLite database

    Parameters
    ----------
    db_file: str
        A path to database file

    Returns
    -------
    conn: Database
        A Database connection object
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """
    Creates table from the `create_table_sql` statement

    Parameters
    ----------
    conn: Database
        Connection database object
    create_table_sql: str
        A `CREATE TABLE` statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(f'create_table: {e}')
    return


def write_to_table(conn, person):
    """
    Create a new record of detected person into the `attendance` table

    Parameters
    ----------
    conn: Database
        Connection database object
    person: Tuple
        Data to be inserted

    Returns
    -------
    cursor.lastrowid:
        The id of last row
    """
    sql = ''' INSERT INTO attendance(name,date,time)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()
    return cur.lastrowid


def exists(conn, data):
    sql = conn.cursor()
    name, day, time = data
    request = 'SELECT * FROM attendance WHERE name=? AND date=? AND time=?'
    cur = sql.execute(request, (name, day, time))
    date_list = cur.fetchall()
    if (len(date_list)):
        return True
    return False


if __name__ == '__main__':
    conn = create_connection("custom.db")
    if conn:
        create_table(conn, sql_create_attendance_table)
        # write_to_table(conn, ("Illia", "14/10/2022", "16:16:16"))
        conn.close()
    else:
        print("Error! Can't create the database")
