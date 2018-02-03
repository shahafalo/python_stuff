import sqlite3
import datetime
import os
import hashlib

DB_PATH = "./date_hash.db"
DB_NAME = "date_hash"
FILES_DB_NAME = "files"
FILES_DB_PATH = "files.db"

CREATE_QUERY = """CREATE TABLE
                    IF NOT EXISTS {} (
                     id integer PRIMARY KEY,
                     file_name text NOT NULL,
                     time text,
                     hash CHAR(64)
                    );""".format(FILES_DB_NAME)


def create_files_db_file():
    """
    This func create the db file and save it under the
    :return: Nothing
    """
    if not os.path.exists(FILES_DB_PATH):
        conn = sqlite3.connect(FILES_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(CREATE_QUERY)
        cursor.close()
        conn.close()
        print "New DB file created in the path:", FILES_DB_PATH
    else:
        print "It seems like that the file already exists."


def add_file(file_path):
    """
    The func will get the file path and will calculate the final hash
    using the time, save it and return it to the user.
    :param file_path: the path of the wanted file
    :return: the final hash
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    first_file_hash = hashlib.sha1()
    first_file_hash.update(data)
    time = datetime.datetime.now()
    time_hash = get_hash_time(time)
    final_hash = calculate_final_hash(first_file_hash, time_hash)
    add_file_to_db(file_path, final_hash, time)
    print "new file added at", time, ":/r/n", file_path, " - ", final_hash


def get_hash_time(time):
    """

    :param time: the wanted time
    :return: the hash from the DB that equal to the time
    """
    # TODO: finish this func
    pass


def calculate_final_hash(file_hash, time_hash):
    """

    :param file_hash:
    :param time_hash:
    :return: the final hash
    """
    # TODO: finish this func
    pass


def add_file_to_db(file_path, file_hash, time):
    """

    :param file_path:
    :param file_hash:
    :param time:
    :return:
    """
    insert_query = "INSERT INTO {}(file_name, time, hash)" \
                   "VALUES('{}','{}','{}')".format(FILES_DB_NAME, file_path, time, file_hash)
    conn = sqlite3.connect(FILES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()
    # TODO: check if this working well

