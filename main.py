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
    initial_sidebar_state="auto")

col1, col2 = st.columns(2)

with col1:
    price_paid = st.number_input("Premium Paid", value=50.0)
    current_underlying_price = st.number_input("Current Price of Underlying", value=30.0)
    time_to_exp_days = st.number_input("Days to Expiry", value=125)
    # call chart
with col2:    
    strike_price = st.number_input("Strike Price", value=40.0)
    risk_free_rate = st.number_input("Risk Free Rate", value=0.01)
    volatility = st.slider("Volatility", 0.0,100.0,0.3)
    # put chart

displayed_price_range = st.slider("Range (%)",1,455,20)
pnl_list = ['P/L $', 'P/L %', 'Value', 'Greeks']
greek_list = ['Delta', 'Theta', 'Gamma', 'Vega', 'Rho']
heatmap_selection = st.selectbox(label="Heatmap Type", options=pnl_list, index=2)

time_list_display = []
if time_to_exp_days < 7:
    time_list_display = [d for d in range(time_to_exp_days,0,-1)]
else:
    time_list_display = [time_to_exp_days - (n*(math.ceil(time_to_exp_days/7))) for n in range(0,7)]
print("time to display: ", time_list_display)
b_scholes = BlackScholes(current_underlying_price, time_to_exp_days, strike_price, risk_free_rate, volatility, displayed_price_range)
if heatmap_selection == 'Greeks':
    greek_selection = st.selectbox(label="Greek", options=greek_list)
    # generate heatmap of greeks
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
    ax_call.set_xlabel('DTE')
    ax_call.set_ylabel('Spot Price')
    
    ax_put.set_title('PUT')
    ax_put.set_xlabel('DTE')
    ax_put.set_ylabel('Spot Price')
    plt.yticks(rotation=0)
    plt.tight_layout()



col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    st.pyplot(fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    st.pyplot(fig_put)
