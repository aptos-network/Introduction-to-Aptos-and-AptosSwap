import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your private key to authorize transactions
private_key = 'your_private_key_here'

# API Endpoints for AptosSwap
swap_url = 'https://aptos-network.pro/api/aptosSwap/swap'
add_liquidity_url = 'https://aptos-network.pro/api/aptosSwap/addLiquidity'
check_liquidity_url = 'https://aptos-network.pro/api/aptosSwap/liquidity'

# Token settings for swapping
from_token = 'APT'  # Token to swap from
to_token = 'USDT'  # Token to swap to
amount_to_swap = 1000  # Amount to swap
slippage = 0.5  # Slippage tolerance in percentage

# Liquidity settings
token_a = 'APT'
token_b = 'USDT'
amount_a = 500
amount_b = 500

# Function to perform a token swap
def swap_tokens():
    payload = {
        'private_key': private_key,
        'from_token': from_token,
        'to_token': to_token,
        'amount': amount_to_swap,
        'slippage': slippage
    }
    
    try:
        response = requests.post(swap_url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            logger.info(f"Swap successful! Transaction Hash: {data['tx_hash']}")
        else:
            logger.error(f"Swap failed: {data['message']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during token swap: {e}")

# Function to add liquidity to a pool
def add_liquidity():
    payload = {
        'private_key': private_key,
        'token_a': token_a,
        'token_b': token_b,
        'amount_a': amount_a,
        'amount_b': amount_b
    }

    try:
        response = requests.post(add_liquidity_url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            logger.info(f"Liquidity added successfully! Transaction Hash: {data['tx_hash']}")
        else:
            logger.error(f"Failed to add liquidity: {data['message']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during liquidity addition: {e}")

# Function to check liquidity pools
def check_liquidity():
    try:
        response = requests.get(check_liquidity_url)
        response.raise_for_status()
        data = response.json()
        logger.info("Liquidity Pool Data:")
        for pool, details in data.items():
            logger.info(f"{pool} - Liquidity: {details['liquidity']} - Price: {details['price']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching liquidity data: {e}")

# Main function to run the bot
def run_bot():
    logger.info("Starting the trading bot...")
    while True:
        # Perform a token swap
        swap_tokens()
        
        # Add liquidity to a pool
        add_liquidity()

        # Check current liquidity pools
        check_liquidity()

        # Sleep for 60 seconds before next cycle
        logger.info("Waiting for next cycle...")
        time.sleep(60)

if __name__ == '__main__':
    run_bot()

