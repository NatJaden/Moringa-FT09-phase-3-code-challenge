from database.connection import get_db_connection
from.author import Author
from.magazine import Magazine

class Article:
    def __init__(self, author, title, magazine):
        if not isinstance(author, Author):
            raise ValueError("author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be an instance of Magazine")
        if not (isinstance(title, str) and 5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")

        self._author_id = author.id
        self._magazine_id = magazine.id
        self._title = title

    @property
    def title(self):
        return self._title

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (author_id, magazine_id, title) VALUES (?,?,?)", (self._author_id, self._magazine_id, self._title))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id =?", (self._author_id,))
        author_row = cursor.fetchone()
        conn.close()
        return Author(author_row['name']) if author_row else None

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id =?", (self._magazine_id,))
        magazine_row = cursor.fetchone()
        conn.close()
        return Magazine(magazine_row['name'], magazine_row['category']) if magazine_row else None