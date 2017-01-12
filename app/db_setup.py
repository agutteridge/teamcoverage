import sqlite3
import ijson


def generate_type_table():
    print('Building Type table...')
    conn = sqlite3.connect('pokemondata.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE types(
           Name TEXT PRIMARY KEY,
           Bug REAL, Dark REAL, Dragon REAL, Electric REAL, Fairy REAL,
           Fighting REAL, Fire REAL, Flying REAL, Ghost REAL, Grass REAL,
           Ground REAL, Ice REAL, Normal REAL, Poison REAL, Psychic REAL,
           Rock REAL, Steel REAL, Water REAL);'''
    )
    conn.commit()

    f = open('./resources/types.txt', 'rb')
    types = ijson.items(f, 'types.item')

    for t in types:
        # Ensure types are in alphabetical order
        sorted_list = sorted(t['atk_effectives'], key=lambda l: l[0])
        _, values = zip(*sorted_list)
        float_values = tuple(map(lambda x: float(x), values))
        col_values = (t['name'],) + float_values
        c.execute(
            '''INSERT INTO types VALUES
               (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''' % locals(),
            col_values)
        conn.commit()

    conn.close()


def generate_dex_table():
    print('Building Dex table...')
    conn = sqlite3.connect('pokemondata.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE dex(
           Name TEXT PRIMARY KEY,
           Type1 TEXT, Type2 TEXT);'''
    )
    conn.commit()

    # Large JSON file; use stream
    stream = ijson.parse(open('./resources/pokemon.txt', 'rb'))

    poke_name = ''
    alts_list = []  # List of lists for alternative forms
    for prefix, event, value in stream:
        if (prefix, event) == ('pokemon.item.name', 'string'):
            poke_name = value
        if (prefix, event) == ('pokemon.item.alts.item.suffix', 'string'):
            data = [poke_name, '', '']
            if value:
                data[0] = poke_name + '-' + value
            alts_list.append(data)
        if (prefix, event) == ('pokemon.item.alts.item.types.item', 'string'):
            current_data = alts_list[-1]
            if not current_data[1]:
                current_data[1] = value
            elif not current_data[2]:
                current_data[2] = value
            else:
                print('More than 2 types for ' + current_data[0])
                raise

        if (prefix, event) == ('pokemon.item', 'end_map'):
            for alt in alts_list:
                c.execute(
                    '''INSERT INTO dex VALUES
                       (?,?,?);''' % locals(),
                    tuple(alt))
                conn.commit()

            # Reset values
            poke_name = ''
            alts_list = []

    conn.close()


def run():
    conn = sqlite3.connect('pokemondata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    if not tables:
        generate_type_table()
        generate_dex_table()
    else:
        if 'types' not in tables[0]:
            generate_type_table()
        if 'dex' not in tables[0]:
            generate_dex_table()


if __name__ == '__main__':
    run()
