import streamlit as st
from src.database import SQLiteArticleManager
from src.milvus import MilvusArticleManager
from src.utils import *


st.set_page_config(page_title='Oncology Journal Article Fetcher & Search', layout='wide')

# Initialize Milvus and MySQL managers with error handling
def initialize_managers():
    try:
        milvus_article_manager = MilvusArticleManager()
    except Exception as e:
        st.warning('Milvus is not running. Please start Milvus and refresh the page.')
        st.stop()

    mysql_article_manager = SQLiteArticleManager()
    # try:
    # except Exception as e:
    #     st.warning('MySQL is not running. Please start MySQL and refresh the page.')
    #     st.stop()

    return milvus_article_manager, mysql_article_manager

# Main function to run the Streamlit app
def main():
    # Initialize managers
    milvus_article_manager, mysql_article_manager = initialize_managers()

    # Streamlit UI Setup
    st.title('Oncology Journal Article Fetcher & Search')

    # Sidebar for navigation
    st.sidebar.header('Navigation')
    app_mode = st.sidebar.selectbox("Choose an option:", ["Search Articles", "Upload Document","Fetch Articles"])

    if app_mode == "Fetch Articles":
        st.subheader('Fetch Latest Articles')
        if st.button('Fetch Articles'):
            # Call your fetch_articles function here
            # fetch_articles()
            st.success('Articles fetched and stored')

    elif app_mode == "Search Articles":
        st.subheader('Search for Articles')
        query = st.text_input('Enter your search query:')

        if st.button('Search'):
            if query:
                article_ids = milvus_article_manager.search_articles(query)
                if article_ids:
                    for article_id in article_ids:
                        article = mysql_article_manager.get_article_details(article_id)
                        if article:
                            st.write(f"**Title**: {article[0]}")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Publication Date**: {article[2]}")
                                st.write(f"**Abstract**: {article[3]}")
                            with col2: 
                                st.write(f"**Author**:")
                                article_authors = article[1].split(", ")
                                for i in range(0,len(article_authors),2):
                                    st.write(f"- {article_authors[i]}, {article_authors[i+1] if i+1 < len(article_authors) else ''}")
                            st.write("---")
                        else:
                            st.warning(f"No details found for article ID: {article_id}")
                else:
                    st.warning('No articles found for the given query.')
            else:
                st.warning('Please enter a query!')

    elif app_mode == "Upload Document":
        pdf_file = st.file_uploader("Upload PDF file.")
        if pdf_file is not None:
            text = extract_text_from_pdf(pdf_file)
            chunks = split_text(text)
            for chunk in chunks:
                mysql_article_manager.insert_words_chunks(chunk)
                chunk_id = mysql_article_manager.get_chunks_id(chunk)
                embeddings = generate_embeddings(chunk)
                milvus_article_manager.insert_words_embedding(chunk_id,embeddings)

            query = st.text_input("search query")
            if query != "":
                chunk_ids = milvus_article_manager.search_document(query)
                st.write(len(chunk_ids))
                for chunk_id in chunk_ids:
                    chunk = mysql_article_manager.get_word_chunks_text(chunk_id)
                    if chunk:
                        st.write(chunk)
                st.write(chunk_ids)
           

if __name__ == "__main__":
    main()
