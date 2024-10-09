import mysql.connector
from src.utils import load_config
from datetime import datetime

class MySQLArticleManager:
    def __init__(self):
        config = load_config()
        self.mysql_config = {
            'user': config['mysql']['user'],
            'password': config['mysql']['password'],
            'host': config['mysql']['host'],
            'database': config['mysql']['database'],
        }
        self.connect()

    def connect(self):
        return mysql.connector.connect(**self.mysql_config)

    def create_mysql_table(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    publication_date DATE,
                    abstract TEXT
                )
            """)
            db.commit()

    def insert_article(self, title, author, publication_date, abstract):
        pub_date = datetime.strptime(publication_date, '%Y-%m-%d').date()  # Assuming the date format is 'YYYY-MM-DD'
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO articles (title, author, publication_date, abstract)
                VALUES (%s, %s, %s, %s)
            """, (title, author, pub_date, abstract))
            db.commit()

    def get_article_details(self, article_id):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT title, author, publication_date, abstract FROM articles WHERE id = %s
            """, (article_id,))
            result = cursor.fetchone()
        return result
    
    def get_article_id(self, title, publication_date):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id FROM articles WHERE title = %s AND publication_date = %s
            """, (title, publication_date))
            result = cursor.fetchone()
        return result[0] if result else None

# Example usage:
# article_manager = MySQLArticleManager()
# details = article_manager.get_article_details(1)
# print(details)
