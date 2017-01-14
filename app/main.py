from flask import Flask, render_template, request

from app import db_setup, database


app = Flask(__name__)
db = ''


def init_db():
    global db
    db = db_setup.run(app.config['TESTING'])


@app.route('/')
def index():
    if not db:
        init_db()
    all_pokes = database.get_all_pokes(db)
    return render_template('index.html', all_pokes=all_pokes)


@app.route('/results')
def results():
    if not db:
        init_db()
    pokes = parse_request(request.args)
    all_data = database.get_types(db, pokes)
    # values = calculator.run(all_data)
    # TODO: write strength/weakness calculator
    return str(all_data)


def parse_request(args):
    poke_names = list(request.args.get('poke' + str(i)) for i in range(1, 7))
    none_removed = list(filter(lambda p: p, poke_names))
    return none_removed


if __name__ == '__main__':
    app.run(debug=True)
