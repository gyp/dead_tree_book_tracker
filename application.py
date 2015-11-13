import sqlite3
from flask import Flask, g, abort
from contextlib import closing
from hashlib import sha256
import isbnlib


application = Flask(__name__)
application.config.from_pyfile('configuration.py')

@application.route('/')
def main_page():
    return 'You need to specify an actual ISBN to do this!'


@application.route('/book/<isbn>/<auth_code>')
def show_book_info(isbn, auth_code):
    check_valid_isbn(isbn)
    check_auth_code(isbn, auth_code)
    book = get_book_info(isbn)
    print(book)
    return 'this is where we will display info about the book with the ISBN %s' % isbn


def check_valid_isbn(isbn):
    if isbnlib.notisbn(isbn):
        application.logger.warning('Tried to request invalid ISBN, isbn=%s', isbn)
        abort(500)


def get_book_info(isbn):
    cur = g.db.execute('SELECT author, title, last_location, current_location, cover_url FROM books WHERE isbn=? LIMIT 1', [isbn])
    row = cur.fetchone()
    if row is None:
        book = init_book(isbn)
    else:
        book = dict(author=row[0], title=row[1], last_location=row[2], current_location=row[3], cover_url=row[4])

    return book


def init_book(isbn):
    book = get_metainfo_for_book(isbn)
    store_book_to_db(isbn, book)
    return book


def get_metainfo_for_book(isbn):
    application.logger.debug('Fetching metainfo for book, ISBN=%s', isbn)
    book = dict(author=None, title=None, last_location=None, current_location=None, cover_url=None)

    metainfo = isbnlib.meta(isbn)
    if metainfo is None:
        return None

    book['author'] = ', '.join(metainfo['Authors'])
    book['title'] = metainfo['Title']

    cover = isbnlib.cover(isbn)
    if cover is not None:
        book['cover_url'] = cover[0]

    return book


def store_book_to_db(isbn, book):
    g.db.execute('INSERT INTO books (isbn, author, title, cover_url) VALUES (?, ?, ?, ?)',
                 [isbn, book['author'], book['title'], book['cover_url']])
    g.db.commit()

def check_auth_code(isbn, auth_code):
    auth_string = '%s XXX %s' % (isbn, application.secret_key)
    expected_auth_code = sha256(auth_string.encode('utf-8')).hexdigest()[:10]
    if expected_auth_code != auth_code:
        application.logger.warning("Invalid auth code for a request; isbn='%s', got_code='%s', expected_code='%s'", isbn, auth_code, expected_auth_code)
        abort(403)


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
