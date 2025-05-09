import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_data(ticker, period="1y", interval="1d"):
    """
    Get stock historical data using yfinance
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Data period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        interval (str): Data interval (e.g., '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
    
    Returns:
        pandas.DataFrame: Historical stock data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            return None
        return hist
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_info(ticker):
    """
    Get general information about a stock
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Stock information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except Exception as e:
        st.error(f"Error fetching stock info: {e}")
        return None

@st.cache_data(ttl=86400)  # Cache data for 1 day
def get_company_overview(ticker):
    """
    Get company overview information
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Company overview information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        overview = {
            "longName": info.get("longName", "N/A"),
            "shortName": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "website": info.get("website", "N/A"),
            "longBusinessSummary": info.get("longBusinessSummary", "N/A"),
            "fullTimeEmployees": info.get("fullTimeEmployees", "N/A"),
            "country": info.get("country", "N/A"),
            "city": info.get("city", "N/A"),
            "address": info.get("address1", "N/A"),
            "logo_url": info.get("logo_url", None),
            "exchange": info.get("exchange", "N/A"),
            "marketCap": info.get("marketCap", "N/A"),
            "currency": info.get("currency", "USD")
        }
        
        return overview
    except Exception as e:
        st.error(f"Error fetching company overview: {e}")
        return None

@st.cache_data(ttl=86400)  # Cache data for 1 day
def get_available_tickers():
    """
    Get a list of popular stock tickers as examples
    
    Returns:
        list: List of popular stock tickers
    """
    popular_tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "META", 
        "TSLA", "NVDA", "JPM", "V", "JNJ",
        "WMT", "PG", "MA", "UNH", "HD",
        "BAC", "XOM", "PFE", "T", "VZ",
        "NFLX", "INTC", "CSCO", "KO", "PEP"
    ]
    return popular_tickers
