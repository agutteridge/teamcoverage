import ijson

from app import database
from app import config


def generate_types_table(db):
    print('Building Type table...')
    created = False

    if 'test' in db:  # ensure db name does not contain 'test'!
        f = open('./resources/test_types.txt', 'rb')
    else:
        f = open('./resources/types.txt', 'rb')

    types = ijson.items(f, 'types.item')

    for t in types:
        # Ensure types are in alphabetical order
        sorted_types = sorted(t['atk_effectives'], key=lambda l: l[0])
        names, values = zip(*sorted_types)

        if not created:
            with_datatypes = list(map(lambda t: (t, 'REAL'), names))
            database.create_table(db, 'types', with_datatypes)
            created = True

        float_values = tuple(map(lambda x: float(x), values))
        col_values = (t['name'],) + float_values
        database.insert(db, 'types', col_values)


def generate_dex_table(db):
    print('Building Dex table...')
    cols = [('Type1', 'TEXT'), ('Type2', 'TEXT')]
    database.create_table(db, 'dex', cols)

    # Large JSON file; use stream
    if 'test' in db:  # ensure db name does not contain 'test'!
        stream = ijson.parse(open('./resources/test_pokemon.txt', 'rb'))
    else:
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
                database.insert(db, 'dex', tuple(alt))

            # Reset values
            poke_name = ''
            alts_list = []


def run(testing):
    if testing:
        current_db = config.TEST_DB
    else:
        current_db = config.DEPLOY_DB

    tables = database.get_tables(current_db)
    if 'types' not in tables:
        generate_types_table(current_db)
    if 'dex' not in tables:
        generate_dex_table(current_db)

    return(current_db)
