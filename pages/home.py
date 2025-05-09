import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.stock_data import get_stock_data, get_stock_info, get_available_tickers
from utils.technical_analysis import calculate_indicators
from assets.stock_images import get_stock_image_url

def show():
    """
    Display the home page of the stock analysis dashboard
    """
    st.title("📈 Stock Analysis Dashboard")
    
    # Get the selected stock from session state
    ticker = st.session_state.selected_stock
    period = st.session_state.time_period
    
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Display main stock chart
        stock_data = get_stock_data(ticker, period=period)
        
        if stock_data is not None and not stock_data.empty:
            # Calculate indicators
            data_with_indicators = calculate_indicators(stock_data)
            
            # Create price chart with volume
            fig = go.Figure()
            
            # Add candlestick chart
            fig.add_trace(go.Candlestick(
                x=data_with_indicators.index,
                open=data_with_indicators['Open'],
                high=data_with_indicators['High'],
                low=data_with_indicators['Low'],
                close=data_with_indicators['Close'],
                name='Price'
            ))
            
            # Add volume chart as a separate subplot
            fig.add_trace(go.Bar(
                x=data_with_indicators.index,
                y=data_with_indicators['Volume'],
                name='Volume',
                marker_color='rgba(0, 0, 255, 0.3)',
                yaxis='y2'
            ))
            
            # Add SMA lines
            fig.add_trace(go.Scatter(
                x=data_with_indicators.index,
                y=data_with_indicators['SMA20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='rgba(255, 165, 0, 0.8)')
            ))
            
            fig.add_trace(go.Scatter(
                x=data_with_indicators.index,
                y=data_with_indicators['SMA50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='rgba(255, 0, 0, 0.8)')
            ))
            
            # Customize layout
            fig.update_layout(
                title=f"{ticker} Stock Price - {period}",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                yaxis2=dict(
                    title="Volume",
                    overlaying="y",
                    side="right",
                    showgrid=False
                ),
                height=500,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show quick stats
            last_price = data_with_indicators['Close'].iloc[-1]
            prev_price = data_with_indicators['Close'].iloc[-2] if len(data_with_indicators) > 1 else last_price
            price_change = last_price - prev_price
            price_change_pct = (price_change / prev_price) * 100 if prev_price > 0 else 0
            
            color = "green" if price_change >= 0 else "red"
            change_prefix = "+" if price_change >= 0 else ""
            
            st.markdown(f"**Latest Price:** ${last_price:.2f} <span style='color:{color};'>{change_prefix}{price_change:.2f} ({change_prefix}{price_change_pct:.2f}%)</span>", unsafe_allow_html=True)
            
        else:
            st.error(f"Could not retrieve data for {ticker}. Please check if the ticker symbol is correct.")
            # Display a stock market image
            st.image(get_stock_image_url('chart', 0), use_column_width=True)
    
    with col2:
        # Display stock information
        info = get_stock_info(ticker)
        
        if info is not None:
            company_name = info.get('longName', ticker)
            
            # Display company name and logo
            st.subheader(company_name)
            
            # Show quick summary
            st.markdown("### Quick Summary")
            
            # Market cap
            market_cap = info.get('marketCap', 'N/A')
            if isinstance(market_cap, (int, float)):
                if market_cap >= 1e9:
                    market_cap_str = f"${market_cap/1e9:.2f}B"
                else:
                    market_cap_str = f"${market_cap/1e6:.2f}M"
            else:
                market_cap_str = "N/A"
                
            # Get sector and industry
            sector = info.get('sector', 'N/A')
            industry = info.get('industry', 'N/A')
            
            # Display key stats
            key_stats = {
                "Sector": sector,
                "Industry": industry,
                "Market Cap": market_cap_str,
                "52W High": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
                "52W Low": f"${info.get('fiftyTwoWeekLow', 'N/A')}",
                "Avg Volume": f"{info.get('averageVolume', 'N/A'):,}"
            }
            
            for key, value in key_stats.items():
                st.markdown(f"**{key}:** {value}")
                
            # Show business summary
            st.markdown("### Business Summary")
            summary = info.get('longBusinessSummary', 'No information available.')
            if len(summary) > 300:
                summary = summary[:300] + "..."
            st.write(summary)
            
            # Show "View More" buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analysis", key="home_analysis"):
                    st.session_state.tab = "Stock Analysis"
                    st.rerun()
            with col2:
                if st.button("Company Info", key="home_company"):
                    st.session_state.tab = "Company Info"
                    st.rerun()
        else:
            st.error(f"Could not retrieve information for {ticker}.")
            
    # Display popular stocks section
    st.markdown("---")
    st.subheader("Popular Stocks")
    
    # Get list of popular tickers
    popular_tickers = get_available_tickers()[:5]
    
    # Create columns for popular stocks
    cols = st.columns(len(popular_tickers))
    
    for i, pop_ticker in enumerate(popular_tickers):
        with cols[i]:
            pop_data = get_stock_data(pop_ticker, period="5d")
            if pop_data is not None and not pop_data.empty:
                # Calculate price change
                last_price = pop_data['Close'].iloc[-1]
                prev_price = pop_data['Close'].iloc[-2] if len(pop_data) > 1 else last_price
                price_change_pct = ((last_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                
                color = "green" if price_change_pct >= 0 else "red"
                change_prefix = "+" if price_change_pct >= 0 else ""
                
                # Create a simple line chart
                fig = px.line(pop_data, x=pop_data.index, y='Close', title=pop_ticker)
                fig.update_layout(
                    height=100,
                    margin=dict(l=0, r=0, t=30, b=0),
                    showlegend=False,
                    xaxis=dict(showticklabels=False),
                    yaxis=dict(showticklabels=False)
                )
                
                # Color the line based on trend
                fig.update_traces(line_color=color)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f"**{pop_ticker}**: ${last_price:.2f} <span style='color:{color};'>({change_prefix}{price_change_pct:.2f}%)</span>", unsafe_allow_html=True)
            else:
                st.write(f"{pop_ticker}: No data")
                
    # Display a disclaimer
    st.markdown("---")
    st.caption("Disclaimer: This information is for educational purposes only and not financial advice.")
