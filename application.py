from flask import Flask, g, render_template, request
from book import Book
from calibre import Calibre

application = Flask(__name__)
application.config.from_pyfile('configuration.py')


@application.route('/')
def main_page():
    return render_template('main_page.html')


@application.route('/<int:id>/')
def show_book_info(id):
    book = Book(g.calibre, id)
    return render_book_info(book)


@application.before_request
def before_request():
    library_path = None
    if 'LIBRARY_PATH' in application.config:
        library_path = application.config['LIBRARY_PATH']
    g.calibre = Calibre(library_path)


def render_book_info(book):
    return render_template('book_info.html', book=book, shelves=application.config['SHELVES'], calibre_url=application.config['CALIBRE_URL'])


@application.route('/<int:id>/update_location', methods=['POST'])
def update_location(id):
    book = Book(g.calibre, id)

    if 'update_person' in request.form:
        new_location = request.form['location']
    else:
        new_location = request.form['shelf']
    book.update_location(new_location)

    return render_book_info(book)


if __name__ == '__main__':
    application.run()
