import configparser
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer



# Load configuration
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

# Fetch and parse the articles
def fetch_articles():
    url = "https://www.nature.com/subjects/oncology"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = article.find('h3', class_='c-card__title').get_text(strip=True)
        author = [author.get_text(strip=True) for author in article.find_all('span', itemprop='name')]
        publication_date = article.find('time', itemprop='datePublished').get('datetime')  # Assuming the date is in 'YYYY-MM-DD' format
        abstract = article.find('div', itemprop='description').find('p').get_text(strip=True) if article.find('div', itemprop='description') else 'No abstract available'
        # insert_article(title, ", ".join(author), publication_date, abstract)

        # Embedding the title and storing in Milvus
        model = SentenceTransformer('all-MiniLM-L6-v2')
        title_embedding = model.encode(title).tolist()
        # article_id = get_article_id(title, publication_date)
        # insert_title_embedding(article_id, title_embedding)
