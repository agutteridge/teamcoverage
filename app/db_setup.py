import ijson

import config
from app import database


def generate_types_table(db):
    print('Building Type table...')

    if 'test' in db:  # ensure db name does not contain 'test'!
        f = open('./resources/test_types.txt', 'rb')
    else:
        f = open('./resources/types.txt', 'rb')

    types = ijson.items(f, 'types.item')
    data = {}
    for t in types:
        for score in t['atk_effectives']:
            data.setdefault(score[0], {})
            data[score[0]][t['name']] = float(score[1])

    type_names = sorted(data.keys())
    cols = list(map(lambda t: (t, 'REAL'), type_names))
    database.create_table(db, 'types', cols)

    all_combos = database.get_type_combos(db)
    for c in all_combos:
        combo = c[0] + '_' + c[1]
        data[combo] = {}
        for t in type_names:
            data[combo][t] = float(data[c[0]][t] * data[c[1]][t])

    data_list = list(map(
        lambda e: tuple([e[0]] + list(e[1].values())),
        data.items()
    ))

    database.insert(db, 'types', data_list, many=True)


def generate_dex_table(db):
    def batch_insert(data_list):
        list_of_tuples = list(map(lambda l: tuple(l), data_list))
        database.insert(db, 'dex', list_of_tuples, many=True)

    print('Building Dex table...')
    cols = [('Type1', 'TEXT'), ('Type2', 'TEXT')]
    database.create_table(db, 'dex', cols)

    # Large JSON file; use stream
    if 'test' in db:
        stream = ijson.parse(open('./resources/test_pokemon.txt', 'rb'))
    else:
        stream = ijson.parse(open('./resources/pokemon.txt', 'rb'))

    poke_name = ''
    data_list = []
    for prefix, event, value in stream:
        if (prefix, event) == ('pokemon.item.name', 'string'):
            poke_name = value
        if (prefix, event) == ('pokemon.item.alts.item.suffix', 'string'):
            data = [poke_name, '', '']
            if value:
                data[0] = poke_name + '-' + value
            data_list.append(data)
        if (prefix, event) == ('pokemon.item.alts.item.types.item', 'string'):
            current_data = data_list[-1]
            if not current_data[1]:
                current_data[1] = value
            elif not current_data[2]:
                current_data[2] = value
            else:
                print('More than 2 types for ' + current_data[0])
                raise

        if (prefix, event) == ('pokemon.item', 'end_map'):
            if len(data_list) > 100:  # Insert batches of ~100
                batch_insert(data_list)
                data_list = []
            poke_name = ''
    if data_list:
        batch_insert(data_list)


def run(testing):
    if testing:
        current_db = config.TEST_DB
    else:
        current_db = config.DEPLOY_DB

    tables = database.get_tables(current_db)
    if 'dex' not in tables:
        generate_dex_table(current_db)
    if 'types' not in tables:
        generate_types_table(current_db)

    return(current_db)
