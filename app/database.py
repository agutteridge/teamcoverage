import sqlite3
from contextlib import contextmanager


@contextmanager
def loan(db):
    conn = sqlite3.connect(db)
    try:
        yield {'conn': conn, 'c': conn.cursor()}
    finally:
        conn.close()


def get_all_names(db, name):
    with loan(db) as ldb:
        ldb['c'].execute(f'SELECT Name FROM {name};')
        return _tuple_to_list(ldb['c'].fetchall(), 0)


def get_damage(db, attk, defend):
    with loan(db) as ldb:
        ldb['c'].execute(f'SELECT {attk} FROM types WHERE Name=?;', (defend,))
        result = ldb['c'].fetchone()[0]
        if result == 0:
            result = 0.125
        return result


def get_types(db, pokes):
    qm = _generate_question_marks(len(pokes))
    with loan(db) as ldb:
        query = f'SELECT * FROM dex WHERE Name IN {qm};'
        ldb['c'].execute(query, pokes)
        return ldb['c'].fetchall()


def get_type_combos(db):
    with loan(db) as ldb:
        ldb['c'].execute(
            '''SELECT Type1, Type2 FROM dex
               WHERE (Type1 <> '' AND Type2 <> '')
               GROUP BY Type1, Type2;''')
        return ldb['c'].fetchall()


def create_table(db, name, columns_datatypes):
    type_str = ', '.join(
        list(map(lambda t: t[0] + ' ' + t[1], columns_datatypes))
    )
    with loan(db) as ldb:
        ldb['c'].execute(
            f'CREATE TABLE {name}(Name TEXT PRIMARY KEY, {type_str});')
        ldb['conn'].commit()


def insert(db, name, col_values, many=False):
    with loan(db) as ldb:
        if many:
            qm = _generate_question_marks(len(col_values[0]))
            query = f'INSERT INTO {name} VALUES {qm};'
            ldb['c'].executemany(query, col_values)
        else:
            qm = _generate_question_marks(len(col_values))
            query = f'INSERT INTO {name} VALUES {qm};'
            ldb['c'].execute(query, col_values)
        ldb['conn'].commit()


def get_tables(db):
    with loan(db) as ldb:
        ldb['c'].execute("SELECT * FROM sqlite_master WHERE type='table';")
        return _tuple_to_list(ldb['c'].fetchall(), 1)


def delete_db(db):
    import os
    try:
        os.remove(os.path.join(os.environ['PWD'], db))
    except FileNotFoundError as err:
        with loan(db) as ldb:
            ldb['c'].execute('DROP TABLE IF EXISTS dex;')
            ldb['c'].execute('DROP TABLE IF EXISTS types;')
            ldb['c'].execute('DROP TABLE IF EXISTS damage;')
            ldb['conn'].commit()
            print(err)  # TODO: log error


def _generate_question_marks(number):
    qms = ', '.join('?' for _ in range(0, number))
    return '(' + qms + ')'


def _tuple_to_list(tups, index):
    return list(map(lambda t: t[index], tups))
