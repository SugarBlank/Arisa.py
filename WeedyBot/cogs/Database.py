from os.path import isfile
from sqlite3 import connect

DB_PATH = "/home/scouri/Programming/Python/Weedy/WeedyBot/database/database.db"
BUILD_PATH = "/home/scouri/Programming/Python/Weedy/WeedyBot/database/build.sql"

connection = connect(DB_PATH, check_same_thread=False)
cursor = connection.cursor()


def with_commit(func):
    def inner_func(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner_func


@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def commit():
    connection.commit()


def close():
    connection.close()


def field(command, *values):
    cursor.execute(command, tuple(values))

    if (fetch := cursor.fetchone()) is not None:
        return fetch[0]


def row(command, *values):
    cursor.execute(command, tuple(values))

    return cursor.fetchone()


def rows(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchall()


def columns(command, *values):
    cursor.execute(command, tuple(values))

    return [item[0] for item in cursor.fetchall()]


def execute(command, *values):
    cursor.execute(command, tuple(values))


def multiexec(command, valueset):
    cursor.executemany(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-0") as script:
        cursor.executescript(script.read())
