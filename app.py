import streamlit as st
from src.news_fetcher import fetch_news
from src.summarizer import summarize_article
from spellchecker import SpellChecker

spell = SpellChecker()

st.set_page_config(page_title="AI News Summarizer", page_icon="📰")
st.title("AI News Summarizer 📰")
st.write("Enter a topic and click the button to get AI-summarized news with sentiment analysis")

query = st.text_input("Enter topic (e.g. AI, startup India, cricket): ")

def is_valid_query(text):
    words = text.strip().split()
    if len(text.strip()) < 3:
        return False
    # Har word check karo ki dictionary mein hai ya nahi
    for word in words:
        if word.lower() not in spell:
            return False
    return True

if st.button("Fetch & Summarize News"):
    if not is_valid_query(query):
        st.error("Please enter a valid topic (real words only, e.g. AI, cricket, startup)")
    else:
        with st.spinner("Fetching news..."):
            articles = fetch_news(query=query)

        if len(articles) == 0:
            st.error("No news found for this topic. Try a different keyword.")
        else:
            st.success(f"Found {len(articles)} articles. Summarizing...")

            for article in articles:
                with st.spinner(f"Summarizing: {article['title'][:50]}..."):
                    result = summarize_article(article["title"], article["description"])

                st.subheader(article["title"])

                col1, col2 = st.columns([1, 2])

                with col1:
                    if article["image"]:
                        st.image(article["image"], width=200)

                with col2:
                    st.write(f"**Source:** {article['source']}")
                    st.write(f"**Summary:** {result['summary']}")

                    sentiment = result["sentiment"]
                    if sentiment == "Positive":
                        st.success(f"Sentiment: {sentiment} 😊")
                    elif sentiment == "Negative":
                        st.error(f"Sentiment: {sentiment} 😞")
                    else:
                        st.info(f"Sentiment: {sentiment} 😐")

                    st.markdown(f"[Read full article]({article['url']})")

                st.divider()