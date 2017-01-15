import os
import sqlite3


def get_all_names(db, name):
    conn, c = _conn_cursor(db)
    c.execute('SELECT Name FROM %(name)s;' % locals())
    result = _tuple_to_list(c.fetchall(), 0)
    conn.close()
    return result


def get_types(db, pokes):
    conn, c = _conn_cursor(db)
    qm = _generate_question_marks(len(pokes))
    c.execute(
        'SELECT * FROM dex WHERE Name IN %(qm)s;' % locals(),
        pokes
    )
    result = c.fetchall()
    conn.close()
    return result


def get_type_combos(db):
    conn, c = _conn_cursor(db)
    c.execute('''SELECT Type1, Type2
                 FROM dex
                 WHERE (Type1 <> '' AND Type2 <> '')
                 GROUP BY Type1, Type2;''')
    result = c.fetchall()
    conn.close()
    return result


def _change_zero(score_list):
    return list(map(lambda e: 0.125 if e == 0 else e, score_list))


def create_table(db, name, columns_datatypes):
    type_str = ', '.join(
        list(map(lambda t: t[0] + ' ' + t[1], columns_datatypes))
    )
    conn, c = _conn_cursor(db)
    c.execute('CREATE TABLE %(name)s(Name TEXT PRIMARY KEY, %(type_str)s);' %
              locals())
    conn.commit()
    conn.close()


def insert(db, name, col_values, many=False):
    conn, c = _conn_cursor(db)
    if many:
        qm = _generate_question_marks(len(col_values[0]))
        c.executemany('INSERT INTO %(name)s VALUES %(qm)s;' % locals(),
                      col_values)
    else:
        qm = _generate_question_marks(len(col_values))
        c.execute('INSERT INTO %(name)s VALUES %(qm)s;' % locals(), col_values)
    conn.commit()
    conn.close()


def get_tables(db):
    conn, c = _conn_cursor(db)
    c.execute("SELECT * FROM sqlite_master WHERE type='table';")
    result = c.fetchall()
    conn.close()
    return _tuple_to_list(result, 1)


def delete_db(db):
    try:
        os.remove(os.path.join(os.environ['PWD'], db))
    except FileNotFoundError as err:
        conn, c = _conn_cursor(db)
        c.execute('DROP TABLE IF EXISTS dex;')
        c.execute('DROP TABLE IF EXISTS types;')
        c.execute('DROP TABLE IF EXISTS damage;')
        conn.commit()
        conn.close()
        print(err)  # TODO: log error


def _generate_question_marks(number):
    qms = ', '.join('?' for _ in range(0, number))
    return '(' + qms + ')'


def _tuple_to_list(tups, index):
    return list(map(lambda t: t[index], tups))


def _conn_cursor(db):
    conn = sqlite3.connect(db)
    return conn, conn.cursor()
