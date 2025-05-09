import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data(ttl=86400)  # Cache data for 1 day
def get_financial_ratios(ticker):
    """
    Get financial ratios and metrics for fundamental analysis
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Dictionary of financial ratios and metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract key metrics
        ratios = {
            # Earnings Metrics
            "EPS": info.get("trailingEPS", np.nan),
            "Forward EPS": info.get("forwardEPS", np.nan),
            "Revenue": info.get("totalRevenue", np.nan),
            "Revenue Per Share": info.get("revenuePerShare", np.nan),
            "Net Profit Margin": info.get("profitMargins", np.nan),
            
            # Valuation Ratios
            "PE Ratio": info.get("trailingPE", np.nan),
            "Forward PE": info.get("forwardPE", np.nan),
            "PEG Ratio": info.get("pegRatio", np.nan),
            "Price to Book": info.get("priceToBook", np.nan),
            "Price to Sales": info.get("priceToSalesTrailing12Months", np.nan),
            "Enterprise Value/EBITDA": info.get("enterpriseToEbitda", np.nan),
            
            # Profitability Ratios
            "Return on Equity": info.get("returnOnEquity", np.nan),
            "Return on Assets": info.get("returnOnAssets", np.nan),
            "Operating Margin": info.get("operatingMargins", np.nan),
            "EBITDA Margin": info.get("ebitdaMargins", np.nan),
            
            # Liquidity & Financial Health
            "Debt to Equity": info.get("debtToEquity", np.nan),
            "Current Ratio": info.get("currentRatio", np.nan),
            "Quick Ratio": info.get("quickRatio", np.nan),
            
            # Efficiency Metrics
            "Asset Turnover": np.nan,  # Not directly available in yfinance
            
            # Dividend Metrics
            "Dividend Yield": info.get("dividendYield", np.nan),
            "Dividend Rate": info.get("dividendRate", np.nan),
            "Payout Ratio": info.get("payoutRatio", np.nan),
            
            # Growth Metrics
            "Earnings Growth": info.get("earningsGrowth", np.nan),
            "Revenue Growth": info.get("revenueGrowth", np.nan),
            
            # Share Statistics
            "Market Cap": info.get("marketCap", np.nan),
            "Shares Outstanding": info.get("sharesOutstanding", np.nan),
            "52 Week High": info.get("fiftyTwoWeekHigh", np.nan),
            "52 Week Low": info.get("fiftyTwoWeekLow", np.nan)
        }
        
        # Format financial numbers
        for key, value in ratios.items():
            if key in ["Revenue", "Market Cap", "Shares Outstanding"]:
                if not pd.isna(value):
                    if value >= 1e9:
                        ratios[key] = f"${value/1e9:.2f}B"
                    elif value >= 1e6:
                        ratios[key] = f"${value/1e6:.2f}M"
                    elif value >= 1e3:
                        ratios[key] = f"${value/1e3:.2f}K"
            elif key in ["Dividend Yield", "Net Profit Margin", "Operating Margin", "EBITDA Margin", 
                       "Return on Equity", "Return on Assets", "Earnings Growth", "Revenue Growth", "Payout Ratio"]:
                if not pd.isna(value):
                    ratios[key] = f"{value:.2%}"
            elif not pd.isna(value):
                ratios[key] = f"{value:.2f}"
                
        return ratios
    except Exception as e:
        st.error(f"Error fetching financial ratios: {e}")
        return None

def get_ratio_description(ratio):
    """
    Get description and interpretation guidelines for a financial ratio
    
    Args:
        ratio (str): Name of the financial ratio
    
    Returns:
        dict: Description and interpretation of the ratio
    """
    descriptions = {
        "EPS": {
            "description": "Earnings Per Share represents a company's profit divided by outstanding shares of common stock.",
            "interpretation": "Higher EPS generally indicates higher profitability. Compare with industry peers and historical trends."
        },
        "PE Ratio": {
            "description": "Price-to-Earnings ratio measures current share price relative to per-share earnings.",
            "interpretation": "Lower P/E may indicate undervaluation. Higher P/E may reflect growth expectations. Compare with industry average."
        },
        "PEG Ratio": {
            "description": "Price/Earnings to Growth ratio factors in a company's expected earnings growth.",
            "interpretation": "PEG < 1 may suggest undervaluation. PEG > 1 may indicate overvaluation relative to growth."
        },
        "Price to Book": {
            "description": "Price-to-Book ratio compares market value to book value.",
            "interpretation": "Lower P/B may indicate undervaluation. Higher values common in companies with intangible assets."
        },
        "Dividend Yield": {
            "description": "Annual dividend payments as a percentage of share price.",
            "interpretation": "Higher yields provide income but may indicate limited growth prospects or unsustainable payouts."
        },
        "Return on Equity": {
            "description": "Measures profitability relative to shareholders' equity.",
            "interpretation": "Higher ROE indicates more efficient use of equity. 15-20% generally considered good."
        },
        "Return on Assets": {
            "description": "Indicates how efficiently a company uses its assets to generate earnings.",
            "interpretation": "Higher ROA shows better asset utilization. Compare within the same industry."
        },
        "Debt to Equity": {
            "description": "Compares total debt to shareholders' equity.",
            "interpretation": "Higher ratios indicate more aggressive financing with debt. Risk varies by industry."
        },
        "Current Ratio": {
            "description": "Measures a company's ability to pay short-term obligations.",
            "interpretation": "Ratio > 1 means current assets exceed current liabilities. 1.5-3.0 generally considered healthy."
        },
        "Operating Margin": {
            "description": "Operating profit as a percentage of revenue.",
            "interpretation": "Higher margins indicate more efficient operations. Compare within industry."
        },
        "Net Profit Margin": {
            "description": "Net profit as a percentage of revenue.",
            "interpretation": "Higher margins indicate more efficient operations after all expenses. Compare within industry."
        },
        "Revenue Growth": {
            "description": "Year-over-year percentage increase in revenue.",
            "interpretation": "Sustained growth indicates expanding business. Compare with industry growth rate."
        },
        "Earnings Growth": {
            "description": "Year-over-year percentage increase in earnings.",
            "interpretation": "Consistent earnings growth typically valued by investors. Should align with revenue growth."
        },
        "Payout Ratio": {
            "description": "Proportion of earnings paid as dividends.",
            "interpretation": "Lower ratios indicate more sustainable dividends and greater reinvestment. Mature companies typically have higher ratios."
        }
    }
    
    return descriptions.get(ratio, {"description": "No description available", "interpretation": "No interpretation available"})
