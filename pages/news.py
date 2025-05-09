import streamlit as st
from utils.generate_sample_news import get_sample_news
import time

def show():
    """
    Display news page
    """
    ticker = st.session_state.selected_stock
    
    st.title(f"📰 Latest News: {ticker}")
    
    # Add a refresh button
    if st.button("🔄 Refresh News"):
        st.rerun()
    
    # Show a loading spinner while fetching news
    with st.spinner(f"Fetching latest news for {ticker}..."):
        # Get sample news directly since APIs are having issues
        news_items = get_sample_news(ticker, limit=10)
    
    if not news_items:
        st.info(f"No news articles found for {ticker}. Try another stock symbol or check back later.")
        return
    
    # Display news articles
    for i, news in enumerate(news_items):
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.subheader(news['title'])
                st.caption(f"Published by {news['publisher']} - {news['published']}")
                st.write(news['summary'])
                
                # Create a button to read the full article (disabled for sample news)
                st.button(f"Read full article", key=f"read_{i}", disabled=True)
            
            with col2:
                # Since we can't display actual images, show a placeholder or icon
                st.markdown("📄")
            
            st.markdown("---")
    
    # Add a disclaimer
    st.caption("**Note:** Sample news headlines are shown. Real-time news integration is under maintenance.")
