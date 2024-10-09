import mysql.connector
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# MySQL configuration
mysql_config = {
    'user': config['mysql']['user'],
    'password': config['mysql']['password'],
    'host': config['mysql']['host'],
    'database': config['mysql']['database'],
}

db = mysql.connector.connect(**mysql_config)


cursor = db.cursor()
cursor.execute("""
    SELECT * from articles;
""")
result = cursor.fetchall()
db.close()
print(result)