from flask_session import Session
from flask import Flask, render_template, request, jsonify, session, redirect
from database import load_books_from_db, load_book_from_db, load_book_from_db_author, load_book_from_db_genre, load_book_from_db_keyword
from database import add_rating_to_db, add_comment_to_db
from database import load_genres_from_db, load_hot_books_from_db, load_trending_books_from_db, load_max_page_from_db
from pdf_to_html import pdf_to_html

app = Flask(__name__)

COMPANY_NAME = "MyBooks"

# Config session

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    hot_books = load_hot_books_from_db()
    trending_book = load_trending_books_from_db()
    return render_template('home.html', name='home', company_name=COMPANY_NAME, hot_books=hot_books, trending_book=trending_book)


@app.route("/<book_url>")
def book_detail(book_url):
    # print(request.url)
    book = load_book_from_db(book_url)
    return render_template('book-detail.html', name='book-detail', company_name=COMPANY_NAME, book=book)


@app.route("/<book_url>/book-<int:page>")
def reading_a_new_book(book_url, page):
    max_page = load_max_page_from_db(book_url)
    content = pdf_to_html(
        f"./static/pdf/{book_url}-books/{book_url}-{page}.pdf")

    session[book_url] = page

    print(page, max_page)

    return render_template('reading-page.html', name='reading-page', company_name=COMPANY_NAME, content=content, book_url=book_url, page=page, max_page=max_page)


@app.route("/continue_reading/<book_url>")
def continue_reading(book_url):
    page = 1
    if book_url in session:
        page = session[book_url]

    return redirect(f'/{book_url}/book-{page}')


@app.route("/all-books")
def all_books():
    # handle books
    books = load_books_from_db()
    return render_template('all-books.html', name='home', company_name=COMPANY_NAME, books=books)


@app.route("/all-genres")
def all_genres():
    # handle genres
    genres = load_genres_from_db()
    return render_template('all-genres.html', name='all-genres', company_name=COMPANY_NAME, genres=genres)


@app.route("/api/books")
def api_books():
    books = load_books_from_db()
    return jsonify(books)


@app.route("/authors/<author>")
def book_author(author):
    books = load_book_from_db_author(author)
    if books == []:
        return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, render="nothing")
    return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, books=books, render="author", author=author)


@app.route("/genres/<genre>")
def book_genre(genre):
    books = load_book_from_db_genre(genre)
    if books == []:
        return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, render="nothing")
    return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, books=books, render="genre", genre=genre)


@app.route("/search")
def search_book():
    keyword = request.args.get('q')
    books = load_book_from_db_keyword(keyword)

    if books == []:
        return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, render="nothing")

    return render_template('book-render.html', name='book-render', company_name=COMPANY_NAME, books=books, render="keyword", keyword=keyword)


@app.route("/add_rating", methods=['POST'])
def add_rating():
    data = request.json
    book_id = data['book_id']
    rating = data['rating']

    add_rating_to_db(book_id, rating)

    return jsonify({'message': 'Rating added successfully'})


@app.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.json
    book_id = data['book_id']
    content = data['content']

    add_comment_to_db(book_id, content)

    return jsonify({'message': 'Rating added successfully'})


@app.route("/features")
def footer_features():
    return render_template('features.html', name='features', company_name=COMPANY_NAME)


@app.route("/faq")
def footer_faq():
    return render_template('faq.html', name='faq', company_name=COMPANY_NAME)


@app.route("/about")
def footer_about():
    return render_template('about.html', name='about', company_name=COMPANY_NAME)


@app.route("/contact")
def footer_contact():
    return render_template('contact.html', name='contact', company_name=COMPANY_NAME)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=False, use_reloader=False)


# show more btn in decs
# URL pathname: home/books/Harry Potter
# comment section
# cs50 favicon.ico error
# star section
# change url to book's name
# author + genre section,
# MyBooks's User
# search (check if author then find author else find title)
# all books page
# more btn genres
# reading page
# bar button of reading page
# sort book in the homepage //star and count comment
# continue reading, must storage page and section of Flask
# footer
# handle if not exist
# deploy
# TODO sort book comment,
# TODO filter function
# TODO 404 error
# ? play music when reading book
