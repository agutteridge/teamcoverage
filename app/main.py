from flask import Flask, render_template, request

from app import database, calc


app = Flask(__name__)
app.config.from_object('config')


def init_db():
    from app import db_setup
    app.config['DATABASE'] = db_setup.run(app.config['TESTING'])


def delete_db():
    database.delete_db(app.config['DATABASE'])
    app.config['DATABASE'] = ''


@app.route('/')
def index():
    if not app.config['DATABASE']:
        init_db()
    all_pokes = database.get_row_names(app.config['DATABASE'], 'dex')
    return render_template('index.html', all_pokes=all_pokes)


@app.route('/results')
def results():
    if not app.config['DATABASE']:
        init_db()
    pokes = parse_request(request.args)
    poke_data = database.get_types(app.config['DATABASE'], pokes)
    results = calc.run_inefficient(app.config['DATABASE'], poke_data)
    return str(list(map(lambda l: l[0:2], sorted(results))))


@app.route('/type/<poke_type>')
def type_page(poke_type):
    if not app.config['DATABASE']:
        init_db()
    poke_type = poke_type.title()
    damage = database.get_row(app.config['DATABASE'], poke_type)
    type_names = database.get_type_names(app.config['DATABASE'])
    type_damage = list(zip(sorted(type_names), damage[1:]))
    data = {'type_name': damage[0], 'damage': type_damage}
    if not data['damage']:
        return 'This type does not exist!'
    else:
        return render_template('type.html', data=data)


def parse_request(args):
    poke_names = list(request.args.get('poke' + str(i)) for i in range(1, 7))
    none_removed = list(filter(lambda p: p, poke_names))
    return none_removed


if __name__ == '__main__':
    app.run(debug=True)
