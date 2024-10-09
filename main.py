import streamlit as st
from src.database import MySQLArticleManager
from src.milvus import MilvusArticleManager

st.set_page_config(page_title='Oncology Journal Article Fetcher & Search', layout='wide')

# Initialize Milvus and MySQL managers with error handling
def initialize_managers():
    try:
        milvus_article_manager = MilvusArticleManager()
    except Exception as e:
        st.warning('Milvus is not running. Please start Milvus and refresh the page.')
        st.stop()

    try:
        mysql_article_manager = MySQLArticleManager()
    except Exception as e:
        st.warning('MySQL is not running. Please start MySQL and refresh the page.')
        st.stop()

    return milvus_article_manager, mysql_article_manager

# Main function to run the Streamlit app
def main():
    # Initialize managers
    milvus_article_manager, mysql_article_manager = initialize_managers()

    # Streamlit UI Setup
    st.title('Oncology Journal Article Fetcher & Search')

    # Sidebar for navigation
    st.sidebar.header('Navigation')
    app_mode = st.sidebar.selectbox("Choose an option:", ["Search Articles","Fetch Articles"])

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

if __name__ == "__main__":
    main()
