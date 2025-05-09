import pandas as pd
import numpy as np
import streamlit as st
import ta
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, ChaikinMoneyFlowIndicator

@st.cache_data
def calculate_indicators(df):
    """
    Calculate technical indicators for a given DataFrame of stock prices
    
    Args:
        df (pandas.DataFrame): DataFrame with OHLCV stock data
    
    Returns:
        pandas.DataFrame: DataFrame with technical indicators added
    """
    if df is None or df.empty:
        return None
    
    # Create a copy to avoid modifying the original dataframe
    result_df = df.copy()
    
    # Calculate Moving Averages
    result_df['SMA20'] = SMAIndicator(close=result_df['Close'], window=20).sma_indicator()
    result_df['SMA50'] = SMAIndicator(close=result_df['Close'], window=50).sma_indicator()
    result_df['SMA200'] = SMAIndicator(close=result_df['Close'], window=200).sma_indicator()
    result_df['EMA20'] = EMAIndicator(close=result_df['Close'], window=20).ema_indicator()
    
    # Calculate MACD
    macd = MACD(close=result_df['Close'])
    result_df['MACD'] = macd.macd()
    result_df['MACD_Signal'] = macd.macd_signal()
    result_df['MACD_Hist'] = macd.macd_diff()
    
    # Calculate RSI
    result_df['RSI'] = RSIIndicator(close=result_df['Close']).rsi()
    
    # Calculate Stochastic Oscillator
    stoch = StochasticOscillator(high=result_df['High'], low=result_df['Low'], close=result_df['Close'])
    result_df['Stoch_K'] = stoch.stoch()
    result_df['Stoch_D'] = stoch.stoch_signal()
    
    # Calculate Bollinger Bands
    bollinger = BollingerBands(close=result_df['Close'])
    result_df['BB_High'] = bollinger.bollinger_hband()
    result_df['BB_Mid'] = bollinger.bollinger_mavg()
    result_df['BB_Low'] = bollinger.bollinger_lband()
    
    # Calculate Average True Range (ATR)
    result_df['ATR'] = AverageTrueRange(high=result_df['High'], low=result_df['Low'], close=result_df['Close']).average_true_range()
    
    # Calculate On Balance Volume
    result_df['OBV'] = OnBalanceVolumeIndicator(close=result_df['Close'], volume=result_df['Volume']).on_balance_volume()
    
    # Calculate Chaikin Money Flow
    result_df['CMF'] = ChaikinMoneyFlowIndicator(high=result_df['High'], low=result_df['Low'], close=result_df['Close'], volume=result_df['Volume']).chaikin_money_flow()
    
    # Support and Resistance (simple calculation using recent highs and lows)
    window = 20
    if len(result_df) >= window:
        result_df['Support'] = result_df['Low'].rolling(window=window).min()
        result_df['Resistance'] = result_df['High'].rolling(window=window).max()
    
    return result_df

def get_indicator_description(indicator):
    """
    Returns description for a technical indicator
    
    Args:
        indicator (str): Name of the indicator
    
    Returns:
        str: Description of the indicator
    """
    descriptions = {
        'SMA': "Simple Moving Average - Average price over specified period. Used to identify trend direction.",
        'EMA': "Exponential Moving Average - Weighted average that gives more importance to recent prices.",
        'MACD': "Moving Average Convergence Divergence - Trend-following momentum indicator that shows the relationship between two moving averages.",
        'RSI': "Relative Strength Index - Momentum oscillator that measures speed and change of price movements on a scale of 0 to 100.",
        'Stochastic': "Stochastic Oscillator - Momentum indicator comparing a security's closing price to its price range over a specific period.",
        'Bollinger': "Bollinger Bands - Volatility bands placed above and below a moving average. Wider bands indicate higher volatility.",
        'ATR': "Average True Range - Measures market volatility by decomposing the entire range of an asset price for that period.",
        'OBV': "On Balance Volume - Uses volume flow to predict changes in stock price. When volume increases without price change, price will eventually jump.",
        'CMF': "Chaikin Money Flow - Measures the amount of Money Flow Volume over a specific period. Values above zero indicate buying pressure, below zero indicate selling pressure.",
        'Support': "Price level where a downtrend is expected to pause due to concentration of demand.",
        'Resistance': "Price level where an uptrend is expected to pause due to concentration of supply."
    }
    
    return descriptions.get(indicator, "No description available.")

def get_indicator_interpretation(df, indicator):
    """
    Provides basic interpretation of current technical indicator values
    
    Args:
        df (pandas.DataFrame): DataFrame with calculated indicators
        indicator (str): Name of the indicator
    
    Returns:
        dict: Dictionary with interpretation and signal
    """
    if df is None or df.empty:
        return {"interpretation": "No data available", "signal": "neutral"}
    
    # Get the last row of data
    last = df.iloc[-1]
    
    interpretations = {
        'SMA': {
            "bullish": last['Close'] > last['SMA50'] and last['SMA20'] > last['SMA50'],
            "bearish": last['Close'] < last['SMA50'] and last['SMA20'] < last['SMA50'],
            "bull_text": "Price is above the 50-day moving average, and the 20-day MA is above the 50-day MA, suggesting an uptrend.",
            "bear_text": "Price is below the 50-day moving average, and the 20-day MA is below the 50-day MA, suggesting a downtrend.",
            "neutral_text": "Price is near the moving averages, suggesting a potential consolidation or trend change."
        },
        'MACD': {
            "bullish": last['MACD'] > last['MACD_Signal'] and last['MACD_Hist'] > 0,
            "bearish": last['MACD'] < last['MACD_Signal'] and last['MACD_Hist'] < 0,
            "bull_text": "MACD line is above the signal line and histogram is positive, suggesting bullish momentum.",
            "bear_text": "MACD line is below the signal line and histogram is negative, suggesting bearish momentum.",
            "neutral_text": "MACD is close to the signal line, indicating potential consolidation or trend change."
        },
        'RSI': {
            "bullish": 40 < last['RSI'] < 70 and last['RSI'] > df['RSI'].iloc[-2],
            "bearish": 30 < last['RSI'] < 60 and last['RSI'] < df['RSI'].iloc[-2],
            "overbought": last['RSI'] > 70,
            "oversold": last['RSI'] < 30,
            "bull_text": "RSI shows increasing momentum in a moderate range, suggesting positive trend.",
            "bear_text": "RSI shows decreasing momentum in a moderate range, suggesting negative trend.",
            "overbought_text": "RSI is above 70, indicating the stock may be overbought and due for a pullback.",
            "oversold_text": "RSI is below 30, indicating the stock may be oversold and due for a bounce."
        },
        'Bollinger': {
            "bullish": last['Close'] > last['BB_Mid'] and last['Close'] < last['BB_High'],
            "bearish": last['Close'] < last['BB_Mid'] and last['Close'] > last['BB_Low'],
            "overbought": last['Close'] > last['BB_High'],
            "oversold": last['Close'] < last['BB_Low'],
            "bull_text": "Price is between the middle band and upper band, suggesting an uptrend.",
            "bear_text": "Price is between the middle band and lower band, suggesting a downtrend.",
            "overbought_text": "Price is above the upper band, indicating potential overbought conditions.",
            "oversold_text": "Price is below the lower band, indicating potential oversold conditions."
        }
    }
    
    if indicator not in interpretations:
        return {"interpretation": "Interpretation not available for this indicator", "signal": "neutral"}
    
    interp = interpretations[indicator]
    
    # Special handling for RSI
    if indicator == 'RSI':
        if interp["overbought"]:
            return {"interpretation": interp["overbought_text"], "signal": "overbought"}
        elif interp["oversold"]:
            return {"interpretation": interp["oversold_text"], "signal": "oversold"}
        elif interp["bullish"]:
            return {"interpretation": interp["bull_text"], "signal": "bullish"}
        elif interp["bearish"]:
            return {"interpretation": interp["bear_text"], "signal": "bearish"}
        else:
            return {"interpretation": "RSI is in neutral territory.", "signal": "neutral"}
    
    # Special handling for Bollinger Bands
    elif indicator == 'Bollinger':
        if interp["overbought"]:
            return {"interpretation": interp["overbought_text"], "signal": "overbought"}
        elif interp["oversold"]:
            return {"interpretation": interp["oversold_text"], "signal": "oversold"}
        elif interp["bullish"]:
            return {"interpretation": interp["bull_text"], "signal": "bullish"}
        elif interp["bearish"]:
            return {"interpretation": interp["bear_text"], "signal": "bearish"}
        else:
            return {"interpretation": "Price is near the middle Bollinger Band, suggesting consolidation.", "signal": "neutral"}
    
    # For other indicators
    else:
        if interp["bullish"]:
            return {"interpretation": interp["bull_text"], "signal": "bullish"}
        elif interp["bearish"]:
            return {"interpretation": interp["bear_text"], "signal": "bearish"}
        else:
            return {"interpretation": interp["neutral_text"], "signal": "neutral"}
