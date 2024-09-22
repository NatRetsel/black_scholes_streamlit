import streamlit as st
import math
import numpy as np
from black_scholes.BlackScholes import BlackScholes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
    "About": "This is a simple app to model various parameters of European options using Black Scholes Model. "
             "By NatRetsel. https://github.com/NatRetsel"
             "https://www.linkedin.com/in/lester-tan-4b135413b/",
    "Report a Bug": "https://github.com/NatRetsel/black_scholes_streamlit"})

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

st.title("Black-Scholes Pricing Model")
linkedin_url = "https://www.linkedin.com/in/lester-tan-4b135413b/"
st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Lester Tan`</a>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    price_paid = st.number_input("Premium Paid", value=15.0)
    current_underlying_price = st.number_input("Current Price of Underlying", value=30.0)
    time_to_exp_days = st.number_input("Days to Expiry", value=125)
    # call chart
with col2:    
    strike_price = st.number_input("Strike Price", value=20.0)
    risk_free_rate = st.number_input("Risk Free Rate", value=0.01)
    volatility = st.slider("Volatility", 0.0,100.0,0.3)
    # put chart

displayed_price_range = st.slider("Range (%)",1,455,100)
pnl_list = ['P/L $', 'P/L %', 'Value', 'Greeks']
greek_list = ['Delta', 'Theta', 'Gamma', 'Vega', 'Rho']
heatmap_selection = st.selectbox(label="Heatmap Type", options=pnl_list, index=2)

time_list_display = []
if time_to_exp_days < 7:
    time_list_display = [d for d in range(time_to_exp_days,0,-1)]
else:
    time_list_display = [time_to_exp_days - (n*(math.ceil(time_to_exp_days/7))) for n in range(0,7)]
#print("time to display: ", time_list_display)
b_scholes = BlackScholes(current_underlying_price, time_to_exp_days, strike_price, risk_free_rate, volatility, displayed_price_range)
if heatmap_selection == 'Greeks':
    greek_selection = st.selectbox(label="Greek", options=greek_list)
    # generate heatmap of greeks
    call_greeks, put_greeks = b_scholes.calculate_greeks(greek_selection)
    fig_call, ax_call = plt.subplots(figsize=(10,7)) # Call
    fig_put, ax_put = plt.subplots(figsize=(10,7)) # Put
    
    sns.heatmap(call_greeks, xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call, cbar=False)
    sns.heatmap(put_greeks, xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put, cbar=False)
    
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Days to Expiry')
    ax_call.set_ylabel('Spot Price')
    
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Days to Expiry')
    ax_put.set_ylabel('Spot Price')
    plt.yticks(rotation=0)
    plt.tight_layout()
# else generate PnL heatmaps
else:
    call_value, put_value = b_scholes.calculate_price()
    fig_call, ax_call = plt.subplots(figsize=(10,7)) # Call
    fig_put, ax_put = plt.subplots(figsize=(10,7)) # Put
    
    
    if heatmap_selection == 'Value':
        sns.heatmap(call_value, xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call, cbar=False)
        sns.heatmap(put_value, xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put, cbar=False)
    else:
        sns.heatmap(BlackScholes.calculate_pnl(call_value,price_paid,heatmap_selection), xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call, cbar=False)
        sns.heatmap(BlackScholes.calculate_pnl(put_value,price_paid,heatmap_selection), xticklabels=time_list_display, yticklabels=np.round(b_scholes.price_range_display, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put, cbar=False)
       
    
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Days to Expiry')
    ax_call.set_ylabel('Spot Price')
    
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Days to Expiry')
    ax_put.set_ylabel('Spot Price')
    plt.yticks(rotation=0)
    plt.tight_layout()



col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.subheader("European call option Heatmap")
    st.pyplot(fig_call)

with col2:
    st.subheader("European put option Heatmap")
    st.pyplot(fig_put)
