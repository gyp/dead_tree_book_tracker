import sqlite3
from contextlib import closing
from hashlib import sha256

from flask import Flask, g, abort, render_template, request

from book import Book

application = Flask(__name__)
application.config.from_pyfile('configuration.py')


@application.route('/')
def main_page():
    return 'You need to specify an actual ISBN to do this!'


@application.route('/book/<isbn>/<auth_code>/')
def show_book_info(isbn, auth_code):
    check_auth_code(isbn, auth_code)
    book = Book(isbn)
    return render_book_info(book)


def check_auth_code(isbn, auth_code):
    auth_string = '%s XXX %s' % (isbn, application.secret_key)
    expected_auth_code = sha256(auth_string.encode('utf-8')).hexdigest()[:10]
    if expected_auth_code != auth_code:
        application.logger.warning("Invalid auth code for a request; isbn='%s', got_code='%s', expected_code='%s'", isbn, auth_code, expected_auth_code)
        abort(403)


def render_book_info(book):
    return render_template('book_info.html', book=book, shelves=application.config['SHELVES'])


@application.route('/book/<isbn>/<auth_code>/update_location', methods=['POST'])
def update_location(isbn, auth_code):
    check_auth_code(isbn, auth_code)
    book = Book(isbn)

    if 'update_person' in request.form:
        new_location = request.form['location']
    else:
        new_location = request.form['shelf']
    book.update_location(new_location)

    return render_book_info(book)


@application.before_request
def before_request():
    g.db = connect_db()


@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def init_db():
    with closing(connect_db()) as db:
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    # TODO: this one should be real database in Amazon RDS
    return sqlite3.connect(application.config['DATABASE'])


if __name__ == '__main__':
    application.run()
