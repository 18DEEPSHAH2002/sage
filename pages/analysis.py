import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.stock_data import get_stock_data
from utils.technical_analysis import calculate_indicators, get_indicator_description, get_indicator_interpretation
from utils.fundamental_analysis import get_financial_ratios, get_ratio_description

def show():
    """
    Display the stock analysis page
    """
    st.title(f"📊 Stock Analysis: {st.session_state.selected_stock}")
    
    # Create tabs for technical and fundamental analysis
    tab1, tab2 = st.tabs(["Technical Analysis", "Fundamental Analysis"])
    
    with tab1:
        show_technical_analysis()
        
    with tab2:
        show_fundamental_analysis()

def show_technical_analysis():
    """
    Display technical analysis section
    """
    ticker = st.session_state.selected_stock
    period = st.session_state.time_period
    
    # Get stock data
    stock_data = get_stock_data(ticker, period=period)
    
    if stock_data is None or stock_data.empty:
        st.error(f"Could not retrieve data for {ticker}. Please check if the ticker symbol is correct.")
        return
    
    # Calculate technical indicators
    data = calculate_indicators(stock_data)
    
    # Create indicator selection
    st.subheader("Technical Indicators")
    
    # Create three columns for organizing indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Trend Indicators")
        show_ma = st.checkbox("Moving Averages (SMA/EMA)", value=True)
        show_macd = st.checkbox("MACD", value=True)
        
    with col2:
        st.markdown("#### Momentum Indicators")
        show_rsi = st.checkbox("RSI", value=True)
        show_stoch = st.checkbox("Stochastic Oscillator")
        
    with col3:
        st.markdown("#### Volatility & Volume")
        show_bb = st.checkbox("Bollinger Bands", value=True)
        show_vol = st.checkbox("Volume Indicators")
    
    # Display the main price chart with selected indicators
    st.subheader("Price Chart with Indicators")
    
    # Create figure with subplots
    fig = make_subplots(rows=3, cols=1, 
                         shared_xaxes=True, 
                         vertical_spacing=0.05,
                         row_heights=[0.6, 0.2, 0.2],
                         subplot_titles=("Price", "Volume", "Indicators"))
    
    # Add candlestick trace for prices
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ), row=1, col=1)
    
    # Add Moving Averages
    if show_ma:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['SMA20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='rgba(255, 165, 0, 0.8)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['SMA50'],
            mode='lines',
            name='SMA 50',
            line=dict(color='rgba(255, 0, 0, 0.8)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['SMA200'],
            mode='lines',
            name='SMA 200',
            line=dict(color='rgba(0, 0, 255, 0.8)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['EMA20'],
            mode='lines',
            name='EMA 20',
            line=dict(color='rgba(128, 0, 128, 0.8)')
        ), row=1, col=1)
    
    # Add Bollinger Bands
    if show_bb:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_High'],
            mode='lines',
            name='BB Upper',
            line=dict(color='rgba(0, 128, 0, 0.5)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Mid'],
            mode='lines',
            name='BB Middle',
            line=dict(color='rgba(0, 128, 0, 0.8)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Low'],
            mode='lines',
            name='BB Lower',
            line=dict(color='rgba(0, 128, 0, 0.5)')
        ), row=1, col=1)
    
    # Add volume bar chart
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker_color='rgba(0, 0, 255, 0.5)'
    ), row=2, col=1)
    
    # Add MACD
    if show_macd:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='rgba(0, 0, 255, 0.8)')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MACD_Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='rgba(255, 0, 0, 0.8)')
        ), row=3, col=1)
        
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['MACD_Hist'],
            name='Histogram',
            marker_color='rgba(0, 255, 0, 0.5)'
        ), row=3, col=1)
    
    # Add RSI
    if show_rsi:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='rgba(255, 0, 0, 0.8)')
        ), row=3, col=1)
        
        # Add RSI reference lines at 70 and 30
        fig.add_trace(go.Scatter(
            x=[data.index[0], data.index[-1]],
            y=[70, 70],
            mode='lines',
            name='Overbought',
            line=dict(color='rgba(255, 0, 0, 0.5)', dash='dash')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=[data.index[0], data.index[-1]],
            y=[30, 30],
            mode='lines',
            name='Oversold',
            line=dict(color='rgba(0, 255, 0, 0.5)', dash='dash')
        ), row=3, col=1)
    
    # Add Stochastic Oscillator
    if show_stoch:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Stoch_K'],
            mode='lines',
            name='%K',
            line=dict(color='rgba(0, 0, 255, 0.8)')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Stoch_D'],
            mode='lines',
            name='%D',
            line=dict(color='rgba(255, 0, 0, 0.8)')
        ), row=3, col=1)
        
        # Add Stochastic reference lines at 80 and 20
        fig.add_trace(go.Scatter(
            x=[data.index[0], data.index[-1]],
            y=[80, 80],
            mode='lines',
            name='Overbought',
            line=dict(color='rgba(255, 0, 0, 0.5)', dash='dash')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=[data.index[0], data.index[-1]],
            y=[20, 20],
            mode='lines',
            name='Oversold',
            line=dict(color='rgba(0, 255, 0, 0.5)', dash='dash')
        ), row=3, col=1)
    
    # Add Volume Indicators
    if show_vol:
        # On Balance Volume normalized
        normalized_obv = (data['OBV'] - data['OBV'].min()) / (data['OBV'].max() - data['OBV'].min()) * 100
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=normalized_obv,
            mode='lines',
            name='OBV (norm)',
            line=dict(color='rgba(128, 0, 128, 0.8)')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['CMF'] * 100,  # Scale to percentage
            mode='lines',
            name='CMF (%)',
            line=dict(color='rgba(0, 128, 128, 0.8)')
        ), row=3, col=1)
    
    # Update layout
    fig.update_layout(
        height=800,
        title=f"{ticker} Technical Analysis - {period}",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display indicator interpretation
    st.subheader("Indicator Analysis")
    
    # Create columns for each category of indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Trend Analysis")
        
        # SMA interpretation
        if show_ma:
            sma_interp = get_indicator_interpretation(data, 'SMA')
            signal_color = {
                "bullish": "green",
                "bearish": "red",
                "neutral": "gray"
            }.get(sma_interp["signal"], "gray")
            
            st.markdown(f"**Moving Averages:** <span style='color:{signal_color};'>{sma_interp['interpretation']}</span>", unsafe_allow_html=True)
            st.markdown(get_indicator_description('SMA'))
            st.markdown("---")
        
        # MACD interpretation
        if show_macd:
            macd_interp = get_indicator_interpretation(data, 'MACD')
            signal_color = {
                "bullish": "green",
                "bearish": "red",
                "neutral": "gray"
            }.get(macd_interp["signal"], "gray")
            
            st.markdown(f"**MACD:** <span style='color:{signal_color};'>{macd_interp['interpretation']}</span>", unsafe_allow_html=True)
            st.markdown(get_indicator_description('MACD'))
    
    with col2:
        st.markdown("#### Momentum & Volatility Analysis")
        
        # RSI interpretation
        if show_rsi:
            rsi_interp = get_indicator_interpretation(data, 'RSI')
            signal_color = {
                "bullish": "green",
                "bearish": "red",
                "overbought": "purple",
                "oversold": "blue",
                "neutral": "gray"
            }.get(rsi_interp["signal"], "gray")
            
            st.markdown(f"**RSI:** <span style='color:{signal_color};'>{rsi_interp['interpretation']}</span>", unsafe_allow_html=True)
            st.markdown(get_indicator_description('RSI'))
            st.markdown("---")
        
        # Bollinger Bands interpretation
        if show_bb:
            bb_interp = get_indicator_interpretation(data, 'Bollinger')
            signal_color = {
                "bullish": "green",
                "bearish": "red",
                "overbought": "purple",
                "oversold": "blue",
                "neutral": "gray"
            }.get(bb_interp["signal"], "gray")
            
            st.markdown(f"**Bollinger Bands:** <span style='color:{signal_color};'>{bb_interp['interpretation']}</span>", unsafe_allow_html=True)
            st.markdown(get_indicator_description('Bollinger'))
            
    # Add a disclaimer
    st.markdown("---")
    st.caption("**Disclaimer:** Technical analysis indicators are tools that help interpret market data. They should not be used in isolation for investment decisions.")

def show_fundamental_analysis():
    """
    Display fundamental analysis section
    """
    ticker = st.session_state.selected_stock
    
    # Get financial ratios
    ratios = get_financial_ratios(ticker)
    
    if ratios is None:
        st.error(f"Could not retrieve fundamental data for {ticker}. This could be due to API limitations or the data might not be available.")
        return
    
    st.subheader("Fundamental Analysis")
    
    # Group ratios by category
    ratio_categories = {
        "Earnings Metrics": ["EPS", "Forward EPS", "Revenue", "Revenue Per Share", "Net Profit Margin"],
        "Valuation Ratios": ["PE Ratio", "Forward PE", "PEG Ratio", "Price to Book", "Price to Sales", "Enterprise Value/EBITDA"],
        "Profitability Ratios": ["Return on Equity", "Return on Assets", "Operating Margin", "EBITDA Margin"],
        "Financial Health": ["Debt to Equity", "Current Ratio", "Quick Ratio"],
        "Dividend Metrics": ["Dividend Yield", "Dividend Rate", "Payout Ratio"],
        "Growth Metrics": ["Earnings Growth", "Revenue Growth"]
    }
    
    # Create columns for each category
    col1, col2 = st.columns(2)
    
    with col1:
        # Display Earnings Metrics
        st.markdown("### Earnings Metrics")
        for ratio in ratio_categories["Earnings Metrics"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
        
        # Display Valuation Ratios
        st.markdown("### Valuation Ratios")
        for ratio in ratio_categories["Valuation Ratios"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
        
        # Display Profitability Ratios
        st.markdown("### Profitability Ratios")
        for ratio in ratio_categories["Profitability Ratios"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
    
    with col2:
        # Display Financial Health Metrics
        st.markdown("### Financial Health")
        for ratio in ratio_categories["Financial Health"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
        
        # Display Dividend Metrics
        st.markdown("### Dividend Metrics")
        for ratio in ratio_categories["Dividend Metrics"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
        
        # Display Growth Metrics
        st.markdown("### Growth Metrics")
        for ratio in ratio_categories["Growth Metrics"]:
            value = ratios.get(ratio, "N/A")
            st.markdown(f"**{ratio}:** {value}")
        
        # Display Share Statistics
        st.markdown("### Share Statistics")
        share_stats = ["Market Cap", "Shares Outstanding", "52 Week High", "52 Week Low"]
        for stat in share_stats:
            value = ratios.get(stat, "N/A")
            st.markdown(f"**{stat}:** {value}")
    
    # Display ratio interpretations
    st.subheader("Key Ratio Interpretations")
    
    # Select ratios to explain
    key_ratios = ["PE Ratio", "PEG Ratio", "Return on Equity", "Debt to Equity", "Current Ratio"]
    
    for ratio in key_ratios:
        if ratio in ratios:
            with st.expander(f"{ratio}: {ratios[ratio]}"):
                ratio_desc = get_ratio_description(ratio)
                st.markdown(f"**Description:** {ratio_desc['description']}")
                st.markdown(f"**Interpretation:** {ratio_desc['interpretation']}")
    
    # Add a disclaimer
    st.markdown("---")
    st.caption("**Disclaimer:** Fundamental analysis data is provided for informational purposes only. Always conduct thorough research before making investment decisions.")
