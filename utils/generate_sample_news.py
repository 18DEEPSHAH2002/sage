import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import random

def get_sample_news(ticker, limit=10):
    """
    Generate sample news items for when real news isn't available
    This is a fallback to ensure users have a good experience
    
    Args:
        ticker (str): Stock ticker symbol
        limit (int): Maximum number of news items to return
    
    Returns:
        list: List of sample news items
    """
    # Company names for common tickers
    companies = {
        'AAPL': 'Apple',
        'MSFT': 'Microsoft',
        'AMZN': 'Amazon',
        'GOOGL': 'Google',
        'META': 'Meta',
        'TSLA': 'Tesla',
        'NVDA': 'NVIDIA',
        'JPM': 'JPMorgan',
        'V': 'Visa',
        'WMT': 'Walmart',
        'JNJ': 'Johnson & Johnson'
    }
    
    company_name = companies.get(ticker, ticker)
    
    # News headline templates
    headlines = [
        "{company} Reports Strong Quarterly Results",
        "{company} Announces New Product Launch",
        "Analysts Upgrade {company} Stock Rating",
        "{company} Expands to New Markets",
        "{company} CEO Discusses Future Growth Strategy",
        "Industry Trends Favor {company}'s Business Model",
        "{company} Partners with Major Technology Provider",
        "Financial Report: {company}'s Revenue Growth Exceeds Expectations",
        "{company} Addresses Recent Market Challenges",
        "Investment Opportunities in {company} Stock",
        "{company} Implements Cost-Cutting Measures",
        "Market Analysts Review {company}'s Performance",
        "{company} Focuses on Sustainable Business Practices",
        "Economic Outlook and Its Impact on {company}",
        "Quarterly Earnings Show {company}'s Resilience"
    ]
    
    # Publishers
    publishers = [
        "Financial Times", 
        "Wall Street Journal", 
        "Bloomberg", 
        "Reuters", 
        "CNBC", 
        "MarketWatch",
        "Yahoo Finance",
        "Investor's Business Daily",
        "Seeking Alpha",
        "The Motley Fool"
    ]
    
    # Generate sample news items
    sample_news = []
    now = datetime.now()
    
    for i in range(min(limit, len(headlines))):
        # Random time in the past 3 days
        random_hours = random.randint(1, 72)
        publish_time = now - timedelta(hours=random_hours)
        formatted_time = publish_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Format headline with company name
        title = headlines[i].format(company=company_name)
        
        # Create summary based on title
        summary = f"This article discusses {title.lower()} and provides insights into the company's performance, market position, and future outlook. Investors seeking information about {company_name} will find valuable analysis in this report."
        
        news_item = {
            'title': title,
            'publisher': random.choice(publishers),
            'link': '#',
            'published': formatted_time,
            'summary': summary
        }
        
        sample_news.append(news_item)
    
    return sample_news