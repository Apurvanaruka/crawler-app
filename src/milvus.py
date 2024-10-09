from src.utils import load_config
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import streamlit as st

class MilvusArticleManager:
    def __init__(self):
        self.config = load_config()
        self.milvus_host = self.config['milvus']['host']
        self.milvus_port = self.config['milvus']['port']
        self.connect_milvus()
        self.create_milvus_collection()


    def connect_milvus(self):
        connections.connect(alias="default", host=self.milvus_host, port=self.milvus_port)

    def create_milvus_collection(self):
        fields = [
            FieldSchema(name="title_embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="article_id", dtype=DataType.INT64, is_primary=True)
        ]
        schema = CollectionSchema(fields, "Oncology Articles Collection")
        collection = Collection(name="oncology_articles", schema=schema)
        collection.create_index(field_name="title_embedding", index_params={
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 1024}
        })
        collection.load()

    def insert_title_embedding(self, article_id, title_embedding):
        collection = Collection("oncology_articles")
        data = [
            [title_embedding],
            [article_id]
        ]
        collection.insert(data)

    def search_articles(self, query):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode(query).tolist()
        collection = Collection("oncology_articles")
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}
        }
        results = collection.search(data=[query_embedding], anns_field="title_embedding", param=search_params, limit=10)
        return [result.id for result in results[0]]  # Return article IDs

