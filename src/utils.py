import configparser
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid



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


def extract_text_from_pdf(pdf_file):
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def split_text(text, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to generate UUIDs
def generate_unique_ids(num):
    return [str(uuid.uuid4()) for _ in range(num)]

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    embeddings = model.encode(chunks).tolist()
    return embeddings
