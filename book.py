from flask import g, current_app, abort
import isbnlib

__author__ = 'gyp'


class Book:
    def __init__(self, isbn):
        self._check_valid_isbn(isbn)
        self.isbn = isbn
        self._load_or_initialize()

    @staticmethod
    def _check_valid_isbn(isbn):
        if isbnlib.notisbn(isbn):
            current_app.logger.warning('Tried to request invalid ISBN, isbn=%s', isbn)
            abort(500)

    def _load_or_initialize(self):
        cur = g.db.execute('SELECT author, title, last_location, current_location, cover_url FROM books WHERE isbn=? LIMIT 1', [self.isbn])
        row = cur.fetchone()
        if row is None:
            self._initialize_as_new()
        else:
            self.author = row[0]
            self.title = row[1]
            self.last_location = row[2]
            self.current_location = row[3]
            self.cover_url=row[4]

    def _initialize_as_new(self):
        self._get_metainfo()
        self._store_to_db()

    def _get_metainfo(self):
        current_app.logger.debug('Fetching metainfo for book, ISBN=%s', self.isbn)

        self._initialize_attributes_to_none()

        metainfo = isbnlib.meta(self.isbn)
        if metainfo is None:
            return

        self.author = ', '.join(metainfo['Authors'])
        self.title = metainfo['Title']

        cover = isbnlib.cover(self.isbn)
        if cover is not None:
            self.cover_url = cover[0]

    def _initialize_attributes_to_none(self):
        self.author = None
        self.title = None
        self.last_location = None
        self.current_location = None
        self.cover_url = None

    def _store_to_db(self):
        g.db.execute('INSERT INTO books (isbn, author, title, cover_url) VALUES (?, ?, ?, ?)',
                     [self.isbn, self.author, self.title, self.cover_url])
        g.db.commit()

    def update_location(self, new_location):
        self.last_location = self.current_location
        self.current_location = new_location
        self._save_location_to_db()

    def _save_location_to_db(self):
        g.db.execute('UPDATE books SET last_location = ?, current_location = ? WHERE isbn = ?',
                     [self.last_location, self.current_location, self.isbn])
        g.db.commit()