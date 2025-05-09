import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from yahooquery import Ticker
from utils.generate_sample_news import get_sample_news

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_news(ticker, limit=10):
    """
    Get news related to a specific stock
    
    Args:
        ticker (str): Stock ticker symbol
        limit (int): Maximum number of news items to return
    
    Returns:
        list: List of news items
    """
    try:
        # First try with yahooquery
        formatted_news = get_news_from_yahooquery(ticker, limit)
        
        # If yahooquery fails or returns empty, try yfinance as backup
        if not formatted_news:
            formatted_news = get_news_from_yfinance(ticker, limit)
            
        # If both API methods fail, use sample news as a last resort
        if not formatted_news:
            st.warning("Unable to fetch real-time news. Showing sample headlines.")
            formatted_news = get_sample_news(ticker, limit)
            
        return formatted_news
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        # Even if all methods fail, provide sample news
        return get_sample_news(ticker, limit)

def get_news_from_yahooquery(ticker, limit=10):
    """Get news using yahooquery"""
    try:
        ticker_obj = Ticker(ticker)
        news = ticker_obj.news(limit)
        
        # Format the news data
        formatted_news = []
        
        if isinstance(news, list):
            for item in news[:limit]:
                # Convert timestamp to datetime
                if 'providerPublishTime' in item:
                    publish_time = datetime.fromtimestamp(item['providerPublishTime'])
                    formatted_time = publish_time.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_time = "Unknown"
                    
                news_item = {
                    'title': item.get('title', 'No title'),
                    'publisher': item.get('publisher', 'Unknown'),
                    'link': item.get('link', '#'),
                    'published': formatted_time,
                    'summary': item.get('summary', 'No summary available')
                }
                formatted_news.append(news_item)
        
        return formatted_news
    except Exception as e:
        st.warning(f"YahooQuery error (trying backup): {e}")
        return []

def get_news_from_yfinance(ticker, limit=10):
    """Get news using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        # Format the news data
        formatted_news = []
        for item in news[:limit]:
            # Convert timestamp to datetime
            if 'providerPublishTime' in item:
                publish_time = datetime.fromtimestamp(item['providerPublishTime'])
                formatted_time = publish_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_time = "Unknown"
                
            news_item = {
                'title': item.get('title', 'No title'),
                'publisher': item.get('publisher', 'Unknown'),
                'link': item.get('link', '#'),
                'published': formatted_time,
                'summary': item.get('summary', 'No summary available')
            }
            formatted_news.append(news_item)
            
        return formatted_news
    except Exception as e:
        st.warning(f"YFinance error: {e}")
        return []

def format_relative_time(timestamp_str):
    """
    Format a timestamp string into a relative time (e.g., "2 hours ago")
    
    Args:
        timestamp_str (str): Timestamp string in format '%Y-%m-%d %H:%M:%S'
    
    Returns:
        str: Relative time string
    """
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
    except:
        return timestamp_str
