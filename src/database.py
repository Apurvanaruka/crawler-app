import sqlite3
from src.utils import load_config
from datetime import datetime

class SQLiteArticleManager:
    def __init__(self):
        self.db_path = 'sqlite.db'  # Hardcoded path to the SQLite database file
        self.connect()
        self.create_article_table()
        self.create_document_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_article_table(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    publication_date DATE,
                    abstract TEXT
                )
            """)
            db.commit()

    def create_document_table(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS word_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chunks TEXT
                )
            """)
            db.commit()

    def insert_article(self, title, author, publication_date, abstract):
        pub_date = datetime.strptime(publication_date, '%Y-%m-%d').date()  # Assuming the date format is 'YYYY-MM-DD'
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO articles (title, author, publication_date, abstract)
                VALUES (?, ?, ?, ?)
            """, (title, author, pub_date, abstract))
            db.commit()
        
    def insert_words_chunks(self, chunk):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO word_chunks (chunks)
                VALUES (?)
            """, (chunk,))
            db.commit()

    def get_word_chunks_text(self, chunks_id):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT chunks FROM word_chunks WHERE id = ?
            """, (chunks_id,))
            result = cursor.fetchall()
        return result        

    
    def get_article_details(self, article_id):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT title, author, publication_date, abstract FROM articles WHERE id = ?
            """, (article_id,))
            result = cursor.fetchone()
        return result
    
    def get_chunks_id(self, chunks):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id FROM word_chunks WHERE chunks = ? 
            """, (chunks,))
            result = cursor.fetchone()
        return result[0] if result else None
  
    def get_article_id(self, title, publication_date):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id FROM articles WHERE title = ? AND publication_date = ?
            """, (title, publication_date))
            result = cursor.fetchone()
        return result[0] if result else None

# Example usage:
# article_manager = SQLiteArticleManager()
# details = article_manager.get_article_details(1)
# print(details)
