from flask import Flask, render_template, request

from app import db_setup, database


app = Flask(__name__)
db = ''


def init_db():
    global db
    db = db_setup.run(app.config['TESTING'])


def delete_db():
    global db
    database.delete_db(db)
    db = ''


@app.route('/')
def index():
    if not db:
        init_db()
    all_pokes = database.get_all_names(db, 'dex')
    return render_template('index.html', all_pokes=all_pokes)


@app.route('/results')
def results():
    if not db:
        init_db()
    pokes = parse_request(request.args)
    poke_data = database.get_types(db, pokes)
    all_data = {}  # Dict of all types, each element is a 6x4 2d tuple
    # Top level: all possible types (dict key) and final score (float)
    # Second level: poke 1-6 types (dict key)
    # Third level: results (tuple) 4 indiv. values
    return str(poke_data)


def parse_request(args):
    poke_names = list(request.args.get('poke' + str(i)) for i in range(1, 7))
    none_removed = list(filter(lambda p: p, poke_names))
    return none_removed


if __name__ == '__main__':
    app.run(debug=True)
