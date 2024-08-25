import streamlit as st
import math
from st_btn_select import st_btn_select

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto")

col1, col2 = st.columns(2)

with col1:
    price_paid = st.number_input("Premium Paid", value=50.0)
    current_underlying_price = st.number_input("Current Price of Underlying", value=100.0)
    time_to_exp_days = st.number_input("Days to Expiry", value=30)
    # call chart
with col2:    
    strike_price = st.number_input("Strike Price", value=100.0)
    risk_free_rate = st.number_input("Risk Free Rate", value=0.05)
    volatility = st.slider("Volatility", 0.0,100.0,0.5)
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


if heatmap_selection == 'Greeks':
    greek_selection = st.selectbox(label="Greek", options=greek_list)
    # generate heatmap of greeks
# else generate PnL heatmaps
