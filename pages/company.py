import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.stock_data import get_company_overview
from utils.fundamental_analysis import get_financial_ratios

def show():
    """
    Display company information page
    """
    ticker = st.session_state.selected_stock
    
    st.title(f"🏢 Company Information: {ticker}")
    
    # Get company information
    company_info = get_company_overview(ticker)
    
    if company_info is None:
        st.error(f"Could not retrieve company information for {ticker}.")
        return
    
    # Display company header
    st.header(company_info.get('longName', ticker))
    st.subheader(company_info.get('sector', 'N/A') + " | " + company_info.get('industry', 'N/A'))
    
    # Create columns for company overview
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Business summary
        st.subheader("Business Summary")
        st.write(company_info.get('longBusinessSummary', 'No business summary available.'))
        
        # Key details in a table
        st.subheader("Key Details")
        
        # Create a DataFrame for the key details
        details = {
            "Website": [company_info.get('website', 'N/A')],
            "Country": [company_info.get('country', 'N/A')],
            "City": [company_info.get('city', 'N/A')],
            "Address": [company_info.get('address', 'N/A')],
            "Full-Time Employees": [f"{company_info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(company_info.get('fullTimeEmployees'), (int, float)) else 'N/A'],
            "Exchange": [company_info.get('exchange', 'N/A')]
        }
        
        details_df = pd.DataFrame(details)
        st.dataframe(details_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Market data
        st.subheader("Market Data")
        market_cap = company_info.get('marketCap', 'N/A')
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1e9:
                market_cap_str = f"${market_cap/1e9:.2f}B"
            else:
                market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = "N/A"
        
        currency = company_info.get('currency', 'USD')
        
        market_data = {
            "Market Cap": market_cap_str,
            "Currency": currency
        }
        
        for key, value in market_data.items():
            st.markdown(f"**{key}:** {value}")
    
    # Get financial ratios for financial health visualization
    financial_ratios = get_financial_ratios(ticker)
    
    if financial_ratios:
        st.subheader("Financial Health Overview")
        
        # Select specific ratios for visualization
        profitability_ratios = {
            "Return on Equity": financial_ratios.get("Return on Equity", "N/A"),
            "Return on Assets": financial_ratios.get("Return on Assets", "N/A"),
            "Operating Margin": financial_ratios.get("Operating Margin", "N/A"),
            "Net Profit Margin": financial_ratios.get("Net Profit Margin", "N/A")
        }
        
        # Convert percentage strings to float values for visualization
        profitability_values = {}
        for key, value in profitability_ratios.items():
            if isinstance(value, str) and "%" in value:
                try:
                    profitability_values[key] = float(value.strip("%")) / 100.0
                except ValueError:
                    profitability_values[key] = 0
            elif isinstance(value, (int, float)):
                profitability_values[key] = value
            else:
                profitability_values[key] = 0
        
        # Create a radar chart for profitability ratios
        categories = list(profitability_values.keys())
        values = list(profitability_values.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Profitability'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.2 if values else 0.1]
                )),
            showlegend=False,
            title="Profitability Metrics"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create columns for additional financial metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Valuation Metrics")
            valuation_metrics = [
                "PE Ratio", "Forward PE", "PEG Ratio", 
                "Price to Book", "Price to Sales"
            ]
            
            for metric in valuation_metrics:
                st.markdown(f"**{metric}:** {financial_ratios.get(metric, 'N/A')}")
        
        with col2:
            st.subheader("Financial Stability")
            stability_metrics = [
                "Debt to Equity", "Current Ratio", "Quick Ratio"
            ]
            
            for metric in stability_metrics:
                st.markdown(f"**{metric}:** {financial_ratios.get(metric, 'N/A')}")
                
        # Create a bar chart for earnings and revenue metrics
        st.subheader("Earnings & Revenue")
        
        earnings_metrics = {
            "EPS": financial_ratios.get("EPS", "N/A"),
            "Forward EPS": financial_ratios.get("Forward EPS", "N/A"),
            "Earnings Growth": financial_ratios.get("Earnings Growth", "N/A"),
            "Revenue Growth": financial_ratios.get("Revenue Growth", "N/A")
        }
        
        # Convert to numeric values for the chart
        earnings_values = {}
        for key, value in earnings_metrics.items():
            if isinstance(value, str):
                try:
                    if "%" in value:
                        earnings_values[key] = float(value.strip("%")) / 100.0
                    else:
                        earnings_values[key] = float(value)
                except ValueError:
                    earnings_values[key] = 0
            elif isinstance(value, (int, float)):
                earnings_values[key] = value
            else:
                earnings_values[key] = 0
        
        # Create a DataFrame for the bar chart
        earnings_df = pd.DataFrame({
            'Metric': list(earnings_values.keys()),
            'Value': list(earnings_values.values())
        })
        
        # Generate bar chart
        fig = px.bar(
            earnings_df, 
            x='Metric', 
            y='Value',
            title="Earnings & Growth Metrics",
            color='Value',
            color_continuous_scale=['red', 'yellow', 'green'],
            labels={'Value': 'Value', 'Metric': 'Metric'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Display additional insights and recommendations
    st.subheader("Company Analysis Insights")
    
    st.write("""
    This section provides an analysis of the company based on the available financial data. The insights
    are generated using the company's financial ratios, market position, and industry context.
    
    Always conduct your own research and consider multiple sources of information before making
    investment decisions. Past performance does not guarantee future results.
    """)
    
    # Add a disclaimer
    st.markdown("---")
    st.caption("**Disclaimer:** Information is provided for educational purposes only and should not be considered as investment advice.")
