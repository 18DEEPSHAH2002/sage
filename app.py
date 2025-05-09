import streamlit as st
from pages import home, analysis, company, news, donate

# Set page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create session state variables if they don't exist
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = "AAPL"
if 'time_period' not in st.session_state:
    st.session_state.time_period = "1y"
if 'tab' not in st.session_state:
    st.session_state.tab = "Home"

# Sidebar with navigation
st.sidebar.title("Stock Analysis Dashboard")

# Stock selection
st.sidebar.subheader("Select a Stock")
symbol_input = st.sidebar.text_input("Enter Stock Symbol", value=st.session_state.selected_stock)
if symbol_input and symbol_input != st.session_state.selected_stock:
    st.session_state.selected_stock = symbol_input.upper()
    st.rerun()

# Time period selection
st.sidebar.subheader("Select Time Period")
time_period = st.sidebar.selectbox(
    "Time Period",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=5  # Default to 1y
)
if time_period != st.session_state.time_period:
    st.session_state.time_period = time_period
    st.rerun()

# Navigation
st.sidebar.subheader("Navigation")
pages = {
    "Home": home,
    "Stock Analysis": analysis,
    "Company Info": company,
    "News": news,
    "Donate": donate
}

selected_page = st.sidebar.radio("Go to", list(pages.keys()))

if selected_page != st.session_state.tab:
    st.session_state.tab = selected_page
    st.rerun()

# Display the selected page
pages[selected_page].show()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2023 Stock Analysis Dashboard")
