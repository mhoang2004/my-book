from MySQLdb.cursors import DictCursor
import MySQLdb
import os
from dotenv import load_dotenv
# from algorithm import longest_common_subsequence

load_dotenv()


def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
        port=int(os.getenv("DATABASE_PORT", 3306)),
        autocommit=True,
        ssl_mode="REQUIRED",
        cursorclass=DictCursor,
        ssl={
            "ssl": "/etc/ssl/cert.pem"
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
        query = """
        SELECT content, 
        CASE
        WHEN TIMESTAMPDIFF(SECOND, time, NOW()) < 60 THEN
            CONCAT(TIMESTAMPDIFF(SECOND, time, NOW()), ' seconds ago')
        WHEN TIMESTAMPDIFF(MINUTE, time, NOW()) < 60 THEN
            CONCAT(TIMESTAMPDIFF(MINUTE, time, NOW()), ' minutes ago')
        WHEN TIMESTAMPDIFF(HOUR, time, NOW()) < 24 THEN
            CONCAT(TIMESTAMPDIFF(HOUR, time, NOW()), ' hours ago')
        WHEN TIMESTAMPDIFF(DAY, time, NOW()) < 30 THEN
            CONCAT(TIMESTAMPDIFF(DAY, time, NOW()), ' days ago')
        WHEN TIMESTAMPDIFF(MONTH, time, NOW()) < 12 THEN
            CONCAT(TIMESTAMPDIFF(MONTH, time, NOW()), ' months ago')
        ELSE
            CONCAT(TIMESTAMPDIFF(YEAR, time, NOW()), ' years ago')
        END AS time_ago
        from books JOIN comments on book_id = books.id WHERE books.id = %s ORDER BY time DESC LIMIT 10;"""
        cursor.execute(query, (id,))
        comments = cursor.fetchall()

        # get ratings
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


def add_comment_to_db(book_id, content):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # get info of the book
        query = "INSERT INTO comments (book_id, content, time) VALUES (%s, %s, CONVERT_TZ(NOW(), 'UTC', '+07:00'));"
        cursor.execute(query, (book_id, content))

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


def load_book_from_db_keyword(keyword):
    connection = None
    cursor = None
    keyword = '%'+keyword.lower()+'%'

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # search query
        query = "SELECT title FROM books JOIN writers ON books.id = writers.book_id JOIN authors ON writers.author_id = authors.id  WHERE LOWER(author) LIKE %s OR LOWER(title) LIKE %s"
        cursor.execute(query, (keyword, keyword))
        titles = (a['title'] for a in cursor.fetchall())

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


def load_genres_from_db():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # search query
        query = "SELECT genre FROM genres GROUP BY genre"
        cursor.execute(query)
        genres = (a['genre'] for a in cursor.fetchall())

        return genres
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


def load_hot_books_from_db():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                books.id,
                title, 
                image_url,
                AVG(rating) AS average_rating
            FROM
                books
            LEFT JOIN
                ratings ON books.id = ratings.book_id
            GROUP BY
                books.id, title, image_url
            ORDER BY
                average_rating DESC
            LIMIT 6;
        """

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


def load_trending_books_from_db():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                books.id,
                title, 
                image_url,
                COUNT(*) AS comments_num
            FROM
                books
            LEFT JOIN
                comments ON books.id = comments.book_id
            GROUP BY
                books.id, title, image_url
            ORDER BY
                comments_num DESC
            LIMIT 6;
        """

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


def load_max_page_from_db(book_url):
    connection = None
    cursor = None
    title = book_url.replace("-", " ").title()

    print("title", title)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "select books_num from books where title = %s"
        cursor.execute(query, (title,))
        results = cursor.fetchall()[0]["books_num"]

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
