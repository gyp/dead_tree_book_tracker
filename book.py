from flask import g, current_app, abort
from calibre import Calibre
__author__ = 'gyp'


class Book:
    def __init__(self, library_path, id):
        self.id = id
        self.library_path = library_path
        self._load_attributes_from_calibre()

    def _load_attributes_from_calibre(self):
        book_in_calibre_db = Calibre.get_book_data(self.library_path, self.id)
        if book_in_calibre_db is None:
            current_app.logger.warning('Requested book page with unknown ID, id=%s', self.id)
            abort(404)

        self.author = book_in_calibre_db['authors']
        self.title = book_in_calibre_db['title']
        try:
            self.current_location = book_in_calibre_db['*location']
        except KeyError:
            self.current_location = None

        tags = book_in_calibre_db['tags']
        self.is_ebook = ('E-book' in tags or 'Kindle' in tags)

    def update_location(self, new_location):
        self.last_location = self.current_location
        self.current_location = new_location
        self._save_location_to_db()

    def _save_location_to_db(self):
        if self.current_location:
            Calibre.set_custom(self.id, "location", self.current_location)
        if self.last_location:
            Calibre.set_custom(self.id, "last_location", self.last_location)
