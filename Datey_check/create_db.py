import sqlite3
import os
import datetime
import hashlib

DB_PATH = "./date_hash.db"
DB_NAME = "date_hash"

CREATE_QUERY = """CREATE TABLE
                    IF NOT EXISTS {} (
                     id integer PRIMARY KEY,
                     time text NOT NULL,
                     hash CHAR(64)
                    );""".format(DB_NAME)


def create_db_file():
    """
    This func create the db file and save it under the
    :return: Nothing
    """
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(CREATE_QUERY)
        cursor.close()
        conn.close()
        print "New DB file created in the path:", DB_PATH
    else:
        print "It seems like that the file already exists."


def fill_db():
    """
    fill the db with the wanted data.
    :return: nothing
    """
    today = datetime.date.today()
    my_datetime = datetime.datetime(year=today.year, month=today.month, day=today.day)
    seconds_in_a_day = 60*60*24  # 86400
    for i in xrange(seconds_in_a_day):
        temp_hash = date_hash(my_datetime)
        write_to_db(my_datetime, temp_hash)
        if i % 1000 == 0 :
            print my_datetime, "-", temp_hash
        my_datetime = my_datetime + datetime.timedelta(0, 1)
        # add a second to the date


def date_hash(date):
    """
    receiving a time and create an hash using it.
    the hash algorithm while be stupid for now but should improve in the future
    TODO: change the hash algorithm to a strong one.
    :param date: a full date time
    :return: the wanted hash
    """
    temp_hash = hashlib.sha1()
    temp_hash.update(str(date))
    return temp_hash.hexdigest()


def write_to_db(my_datetime, temp_hash):
    """

    :return:
    """
    insert_query = "INSERT INTO {}(time, hash)" \
                   "VALUES('{}','{}')".format(DB_NAME, str(my_datetime), temp_hash)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()


print "start", datetime.datetime.now()
fill_db()
print "finish", datetime.datetime.now()
