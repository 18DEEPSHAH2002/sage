import streamlit as st

def show():
    """
    Display donation page with PayPal integration
    """
    st.title("💰 Support Our Project")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Why Donate?
        
        Thank you for using our Stock Analysis Dashboard! This project is developed and maintained with passion and dedication. 
        Your support allows us to:
        
        * Continue adding new features and improvements
        * Maintain and update data sources
        * Keep the service running for everyone to use
        * Expand our analysis tools and indicators
        
        Every contribution, no matter the size, makes a significant difference and is deeply appreciated!
        """)
        
        st.markdown("""
        ### Feature Roadmap
        
        Your donations will help us implement these upcoming features:
        
        * Portfolio tracking and management
        * Advanced screening tools
        * Customizable watchlists
        * Enhanced technical analysis
        * Sentiment analysis from news
        * Mobile application development
        """)
    
    with col2:
        st.markdown("""
        ### Make a Donation
        
        Choose an amount to donate via PayPal:
        """)
        
        # Donation amount selection
        donation_amount = st.selectbox(
            "Select donation amount",
            ["$5.00", "$10.00", "$25.00", "$50.00", "$100.00", "Custom amount"]
        )
        
        if donation_amount == "Custom amount":
            custom_amount = st.number_input("Enter custom amount ($USD)", min_value=1.0, step=1.0, value=15.0)
            donation_amount = f"${custom_amount:.2f}"
        
        # Display PayPal donation button
        st.markdown("""
        ### Proceed to PayPal
        
        Click the button below to complete your donation through PayPal's secure system:
        """)
        
        # Replace YOUR_BUTTON_ID with an actual PayPal button ID in a real implementation
        paypal_button_html = f"""
        <form action="https://www.paypal.com/donate" method="post" target="_blank">
          <input type="hidden" name="business" value="your-paypal-email@example.com" />
          <input type="hidden" name="amount" value="{donation_amount.replace('$', '')}" />
          <input type="hidden" name="currency_code" value="USD" />
          <input type="hidden" name="item_name" value="Stock Analysis Dashboard Donation" />
          <input type="submit" style="background-color:#0070BA; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-size:16px;" value="Donate {donation_amount} with PayPal" />
        </form>
        """
        
        st.markdown(paypal_button_html, unsafe_allow_html=True)
        
        st.caption("You will be redirected to PayPal to complete your donation securely.")
        
        # Alternative payment methods
        st.markdown("""
        ### Other Ways to Support
        
        * Star our project on GitHub
        * Share with friends and colleagues
        * Provide feedback and suggestions
        * Report bugs and issues
        """)
    
    # Add thank you message
    st.markdown("---")
    st.markdown("""
    ### Thank You for Your Support!
    
    Every contribution helps us continue developing and improving this tool for the community.
    """)
    
    # Add a disclaimer
    st.caption("**Note:** This is a donation, not a payment for services or a financial investment.")
