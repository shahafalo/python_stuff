import win32crypt
import sqlite3
import os
import datetime

FOLDER_PATH = os.getenv('APPDATA') + "\Shahafalo"
PASSWORD_MANAGER_DB_PATH = FOLDER_PATH + "\Password_manager.db"
HEADERS = ['service', 'username', 'password', 'insert_date']
DB_NAME = "auth"
CREATE_QUERY = """CREATE TABLE
                    IF NOT EXISTS {} (
                     id integer PRIMARY KEY,
                     service text NOT NULL,
                     username text,
                     password CHAR(64),
                     insert_date text
                    );""".format(DB_NAME)


def create_passwords_file():
    """
    This func create the passwords manager file and save it under the
    FOLDER_PATH
    :return: Nothing
    """
    if not os.path.isdir(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    if not os.path.exists(PASSWORD_MANAGER_DB_PATH):
        conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(CREATE_QUERY)
        cursor.close()
        conn.close()
        print "New password manager file created in the path:", PASSWORD_MANAGER_DB_PATH
    else:
        print "It seems like that the file already exists."


def check_if_exists(service='', username=''):
    """
    Check if the entered username or service exists in the table.
    :param service:
    :param username:
    :return:
    """
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    query = "select count(*) from auth where service = '{}' and username = '{}'".format(service, username)
    q = cursor.execute(query)
    # check if there are more then 0 rows in the DB with this service and username
    return q.fetchone()[0] > 0


def add_password(service, username, password):
    """
    This func gets parameters for the file and add it.
    :param service: The wanted service, ex: 'GMAIL'
    :param username:
    :param password: Password in plain text, it will decrypt before saving.
    :return: Nothing
    """
    date = str(datetime.date.today())
    password = win32crypt.CryptProtectData(password).encode("hex")
    insert_query = "INSERT INTO auth(service, username, password, insert_date)" \
                   "VALUES('{}','{}','{}','{}')".format(service, username, password, date)
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_password(service, username):
    """
    Getting the password of the wanted service or username from the DB
    :param service: the name of the wanted service, ex. "google"
    :param username:
    :return: The wanted password in plain text
    """
    if not check_if_exists(service, username):
        print "seems like there is no username and service like that"
        return None
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    query = "select password from auth where service = '{}' and username = '{}'".format(service, username)
    q = cursor.execute(query)
    password = q.fetchone()[0].decode("hex")
    password = win32crypt.CryptUnprotectData(password)[1]
    # CryptUnprotectData return tuple and I want only the password.
    return password


def update_password(service, username, password):
    """
    Updating the password of the service and username according to the input.
    :param service:
    :param username:
    :param password: password in plain text
    :return: Nothing
    """
    password = win32crypt.CryptProtectData(password).encode("hex")
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    query = "UPDATE auth SET password = '{}' where service = '{}' and username = '{}'".format(password, service, username)
    cursor.execute(query)
    conn.commit()


def get_all_services():
    """

    :return:
    """
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    q = cursor.execute("select distinct service from auth")
    return q.fetchall()


def get_all_usernames():
    """

    :return:
    """
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    q = cursor.execute("select service, username from auth")
    return q.fetchall()


def get_username_by_service(service):
    """

    :return:
    """
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    q = cursor.execute("select username from auth where service = '{}'".format(service))
    return q.fetchall()[0][0]


def __select_all__():
    """
    private function that enables to print all the data from the DB.
    :return: list of all the data.
    """
    conn = sqlite3.connect(PASSWORD_MANAGER_DB_PATH)
    cursor = conn.cursor()
    q = cursor.execute("select * from auth")
    return q.fetchall()
