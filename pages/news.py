import streamlit as st
from utils.news import get_stock_news, format_relative_time

def show():
    """
    Display news page
    """
    ticker = st.session_state.selected_stock
    
    st.title(f"📰 Latest News: {ticker}")
    
    # Get news for the selected stock
    news_items = get_stock_news(ticker, limit=20)
    
    if not news_items:
        st.info(f"No news articles found for {ticker}. Try another stock symbol or check back later.")
        return
    
    # Display news articles
    for i, news in enumerate(news_items):
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.subheader(news['title'])
                st.caption(f"Published by {news['publisher']} - {format_relative_time(news['published'])}")
                st.write(news['summary'])
                
                # Create a button to read the full article
                if st.button(f"Read full article", key=f"read_{i}"):
                    st.markdown(f"<a href='{news['link']}' target='_blank'>Click here if not automatically redirected</a>", unsafe_allow_html=True)
                    st.markdown(f'<script>window.open("{news["link"]}", "_blank");</script>', unsafe_allow_html=True)
            
            with col2:
                # Since we can't display actual images, show a placeholder or icon
                st.markdown("📄")
            
            st.markdown("---")
    
    # Add a disclaimer
    st.caption("**Disclaimer:** News articles are provided for informational purposes only.")
