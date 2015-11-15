from flask import Flask, g, abort, render_template, request
from book import Book

application = Flask(__name__)
application.config.from_pyfile('configuration.py')


@application.route('/')
def main_page():
    return 'You need to specify a book ID to do this!'


@application.route('/<int:id>/')
def show_book_info(id):
    book = Book(id)
    return render_book_info(book)


def render_book_info(book):
    return render_template('book_info.html', book=book, shelves=application.config['SHELVES'], calibre_url=application.config['CALIBRE_URL'])


@application.route('/<int:id>/update_location', methods=['POST'])
def update_location(id):
    book = Book(id)

    if 'update_person' in request.form:
        new_location = request.form['location']
    else:
        new_location = request.form['shelf']
    book.update_location(new_location)

    return render_book_info(book)


if __name__ == '__main__':
    application.run()
