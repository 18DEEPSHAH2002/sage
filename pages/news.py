import streamlit as st
from utils.news import get_stock_news, format_relative_time
import time

def show():
    """
    Display news page
    """
    ticker = st.session_state.selected_stock
    
    st.title(f"📰 Latest News: {ticker}")
    
    # Add a refresh button
    if st.button("🔄 Refresh News"):
        # Use st.experimental_memo.clear() to clear all cache
        # Note: we don't do individual cache clearing as it can be complex
        from streamlit import cache_data
        cache_data.clear()
        st.rerun()
    
    # Show a loading spinner while fetching news
    with st.spinner(f"Fetching latest news for {ticker}..."):
        # Get news for the selected stock
        news_items = get_stock_news(ticker, limit=20)
    
    if not news_items:
        st.info(f"No news articles found for {ticker}. Try another stock symbol or check back later.")
        
        # Add some troubleshooting steps for the user
        with st.expander("Troubleshooting Steps"):
            st.markdown("""
            If you're not seeing any news, try these steps:
            1. Click the "🔄 Refresh News" button above
            2. Try a different stock symbol (popular ones like AAPL, MSFT, or AMZN often have more news)
            3. Wait a few minutes and try again
            """)
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
