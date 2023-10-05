import streamlit as st
import alpaca_trade_api as tradeapi
import datetime
import threading
import time
import pickle as pkl



def place_order(symbol,quantity,side,order_type,api):
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force='gtc'
        )
        st.write(f'Order for {quantity} shares of {symbol} placed successfully.')
    except Exception as e:
        st.write(f'Error placing order: {str(e)}')
# Set dark theme
st.set_page_config(page_title="Alpaca Trading App", layout="wide")

# Create a dictionary to store user credentials
user_credentials = {}

# Create a dictionary for stock orders (buy/sell)
stocks_dict = pkl.load(open("stocks_invest.pkl","rb"))

# Function to verify Alpaca credentials
def verify_credentials(api_key, api_secret):
    try:
        api = tradeapi.REST(api_key, api_secret, base_url="https://paper-api.alpaca.markets")
        account_info = api.get_account()
        return True
    except Exception as e:
        return False

# Streamlit UI
st.title("Alpaca Trading App")

# Input fields for Alpaca credentials
api_key = st.text_input("Enter your Alpaca API Key")
api_secret = st.text_input("Enter your Alpaca API Secret", type="password")

# Save credentials when the "Save Credentials" button is clicked
if st.button("Save Credentials"):
    if verify_credentials(api_key, api_secret):
        user_credentials["api_key"] = api_key
        user_credentials["api_secret"] = api_secret
        st.success("Credentials saved successfully!")
    else:
        st.error("Invalid credentials. Please check and try again.")

# Start automated trading when the "Start Trading" button is clicked
if st.button("Start Trading"):

    st.write("Automated trading started...")
    api = tradeapi.REST(api_key, api_secret, base_url='https://paper-api.alpaca.markets')
    st.write(datetime.datetime.now().second == True)

    if True:
        # Execute buy orders
        st.write("Buying stocks...")
        for stock in stocks_dict["buy"]:
            place_order(stock,1,"buy","market",api)

        for stock in stocks_dict["sell"]:
            place_order(stock,1,"sell","market",api)
            
            

    

    # Check if it's 3 minutes before 1:00 AM
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 57:
        # Implement sell orders or delivery logic
        st.write("Selling or delivering stocks...")
        for stock in stocks_dict["buy"]:
            place_order(stock,1,"sell","market",api)
        for stock in stocks_dict["sell"]:
            place_order(stock,1,"buy","market",api)
            
            

    # Sleep for 1 second (simulating real-time trading)
    time.sleep(1)



# Stop trading when the "Stop Trading" button is clicked
if st.button("Stop Trading"):
    # Implement logic to stop trading
    # For simplicity, we'll print a message here
    api = tradeapi.REST(api_key, api_secret, base_url='https://paper-api.alpaca.markets')
    for stock in stocks_dict["buy"]:
        place_order(stock,1,"sell","market",api)
    for stock in stocks_dict["sell"]:
        place_order(stock,1,"buy","market",api)
    st.write("Trading stopped.")

# Display buy and sell orders
st.subheader("Buy Orders")
st.write(stocks_dict["buy"])

st.subheader("Sell Orders")
st.write(stocks_dict["sell"])
