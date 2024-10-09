CREATE DATABASE IF NOT EXISTS oncology_articles_db;
GRANT ALL PRIVILEGES ON oncology_articles_db.* TO 'root'@''%'' IDENTIFIED BY 'root';
FLUSH PRIVILEGES;