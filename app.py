from flask import Flask, render_template, request, jsonify
from database import load_books_from_db, load_book_from_db, add_rating_to_db, load_book_from_db_author, load_book_from_db_genre

app = Flask(__name__)

COMPANY_NAME = "MyBooks"


@app.route("/")
def home():
    books = load_books_from_db()
    return render_template('home.html', name='home', company_name=COMPANY_NAME, books=books)


@app.route("/<book_url>")
def book_detail(book_url):
    # print(request.url)
    book = load_book_from_db(book_url)

    return render_template('book-detail.html', name='book-detail', company_name=COMPANY_NAME, book=book)


@app.route("/api/books")
def api_books():
    books = load_books_from_db()
    return jsonify(books)


@app.route("/<book_name>/reading")
def reading_book(book_name):
    # print(request.url)
    book = load_books_from_db()
    return render_template('reading-page.html', name='reading-page', company_name=COMPANY_NAME, book=book)


@app.route("/authors/<author>")
def book_author(author):
    books = load_book_from_db_author(author)
    return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, books=books, render="author", author=author)


@app.route("/genres/<genre>")
def book_genre(genre):
    books = load_book_from_db_genre(genre)
    return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, books=books, render="genre", genre=genre)


@app.route("/add_rating", methods=['POST'])
def add_rating():
    data = request.json
    book_id = data['book_id']
    rating = data['rating']

    add_rating_to_db(book_id, rating)

    return jsonify({'message': 'Rating added successfully'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=False, use_reloader=False)


# show more btn in decs
# URL pathname: home/books/Harry Potter
# comment section
# cs50 favicon.ico error
# star section
# change url to book's name
# author + genre section,
# TODO comment_section (time, add block comment),
# TODO sort book comment,
# TODO search
# TODO reading page
# TODO more btn genres
# TODO handle if not exist
# TODO all books page
# ? play music when reading book
# Yawawe language
# {{ ', '.join(book.genres) }}
