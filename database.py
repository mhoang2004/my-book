from MySQLdb.cursors import DictCursor
import MySQLdb
import os
from dotenv import load_dotenv
load_dotenv()


def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        cursorclass=DictCursor,
        ssl={
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    )


def load_books_from_db():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """SELECT id, title, image_url FROM books"""
        cursor.execute(query)
        results = cursor.fetchall()

        # for row in results:
        # print(row) # Do something with the retrieved data

        return results
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection when done
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def load_book_from_db(book_url):
    connection = None
    cursor = None

    book_title = book_url.replace("-", " ").title()
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # get id of the book
        query = "SELECT books.id FROM books WHERE books.title = %s;"
        cursor.execute(query, (book_title,))
        id = int(cursor.fetchall()[0]["id"])

        # get info of the book
        query = "SELECT books.id, title, image_url, book_description, book_source, state FROM books WHERE books.id = %s;"
        cursor.execute(query, (id,))
        book = cursor.fetchall()[0]

        # get info of the author
        query = "SELECT author FROM books JOIN writers ON books.id = writers.book_id JOIN authors ON writers.author_id = authors.id WHERE books.id = %s;"
        cursor.execute(query, (id,))
        authors = [a['author'] for a in cursor.fetchall()]

        # get genres
        query = "SELECT genre from books JOIN genres on book_id = books.id WHERE books.id = %s;"
        cursor.execute(query, (id,))
        genres = [a['genre'] for a in cursor.fetchall()]

        # get comments
        query = "SELECT content from books JOIN comments on book_id = books.id WHERE books.id = %s LIMIT 10;"
        cursor.execute(query, (id,))
        comments = [a['content'] for a in cursor.fetchall()]

        # get ratings
        # use AVG function of mysql
        query = "SELECT AVG(rating) AS rating, COUNT(rating) AS votes from books JOIN ratings on book_id = books.id WHERE books.id = %s"
        cursor.execute(query, (id,))
        ratings = cursor.fetchall()[0]

        # code to combine books and authors
        book["authors"] = authors
        book["genres"] = genres
        book["comments"] = comments
        book["rating"] = ratings["rating"]
        book["votes"] = ratings["votes"]

        # for row in results:
        # print(row) # Do something with the retrieved data

        return book
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection when done
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def add_rating_to_db(book_id, rating):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # get info of the book
        query = "INSERT INTO ratings (book_id, rating) VALUES (%s, %s);"
        cursor.execute(query, (book_id, rating))

        # for row in results:
        # print(row) # Do something with the retrieved data

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection when done
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def load_book_from_db_author(author):
    connection = None
    cursor = None
    author_name = author.replace("-", " ").title()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # get info of the book
        query = "SELECT books.title FROM books JOIN writers ON books.id = writers.book_id JOIN authors ON writers.author_id = authors.id WHERE authors.author = %s;"
        cursor.execute(query, (author_name,))
        titles = [a['title'] for a in cursor.fetchall()]

        books = []

        for title in titles:
            books.append(load_book_from_db(title))

        print(titles)

        return books
        # for row in results:
        # print(row) # Do something with the retrieved data

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection when done
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def load_book_from_db_genre(genre):
    connection = None
    cursor = None
    genre_name = genre.replace("-", " ").title()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # get info of the book
        query = "SELECT books.title from books JOIN genres on book_id = books.id WHERE genre = %s"
        cursor.execute(query, (genre_name,))
        titles = [a['title'] for a in cursor.fetchall()]

        books = []

        for title in titles:
            books.append(load_book_from_db(title))

        return books
        # for row in results:
        # print(row) # Do something with the retrieved data

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection when done
        if cursor:
            cursor.close()
        if connection:
            connection.close()
