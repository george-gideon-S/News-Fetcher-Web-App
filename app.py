import streamlit as st
import requests
import datetime

# Define your API key (replace 'YOUR_API_KEY' with your actual API key)
API_KEY = "YOUR_API_KEY"

# Today's date
from_ = datetime.date.today()
# yesterday's date & converted to str
to_ = str(from_ - datetime.timedelta(days=1))
# from_ converted to str
from_ = str(from_)

# Language mapping (short forms to full forms)
language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
}

# Streamlit app title and header
st.title("News Fetcher App")
st.header("Get the Latest News")

# Define the base URL for the News API
base_url = 'https://newsapi.org/v2/everything'

# Input for user to provide keyword for search
search_keyword = st.text_input("Enter a keyword for news search", "ai")

# Input for user to choose the language
selected_language = st.selectbox("Select a language for the news", list(language_mapping.values()))

# Input for user to choose the sorting option
sort_by = st.selectbox("Sort by", ["relevancy", "popularity", "publishedAt", "top"])

# Input for user to specify the number of articles to retrieve
num_articles = st.number_input("Number of articles to retrieve", 1, 100, 10)

# Convert selected_language (full form) to the short form
language = [key for key, value in language_mapping.items() if value == selected_language][0]

# Button to trigger the API request
if st.button("Fetch News"):
    params = {
        'apiKey': API_KEY,
        'q': search_keyword,
        'language': language,
        'from': from_,
        'to': to_,
        'sortBy': sort_by,
        'pageSize': num_articles
    }

    # Make the request to the API
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        if articles:
            for article in articles:
                st.subheader(article['title'])
                st.write(f"Source: {article['source']['name']}")
                st.write(f"URL: {article['url']}")
                st.write("\n---")
        else:
            st.warning("No articles were found for the specified parameters.")
    else:
        st.error(f"Failed to retrieve articles (Status code: {response.status_code})")