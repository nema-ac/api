from flask import Flask
from flask_cors import CORS
import csv
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
wallet_data = {}
TOTAL_SUPPLY = 1_000_000_000  # 1 billion tokens
AIRDROP_PERCENTAGE = 0.6      # 60% of total supply for airdrop

def load_wallet_data():
    global wallet_data
    csv_path = os.path.join('static', 'drop', 'wallets.csv')

    if not os.path.exists(csv_path):
        logger.error(f"Wallet data file not found at: {csv_path}")
        raise FileNotFoundError(f"Wallet data file not found at: {csv_path}")

    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            all_rows = list(reader)

            if not all_rows:
                logger.warning("Wallet data file is empty")
                wallet_data = {}
                return

            # First pass: calculate total balance
            try:
                total_balance = sum(float(row['balance']) for row in all_rows)
                if total_balance <= 0:
                    logger.error("Total balance must be greater than 0")
                    raise ValueError("Total balance must be greater than 0")

                # Second pass: calculate projected amounts
                wallet_data = {
                    row['wallet']: {
                        'balance': float(row['balance']),
                        'projected_amount': (float(row['balance']) / total_balance) * TOTAL_SUPPLY * AIRDROP_PERCENTAGE
                    }
                    for row in all_rows
                }
                logger.info(f"Successfully loaded {len(wallet_data)} wallet records")

            except ValueError as ve:
                logger.error(f"Invalid balance value in CSV: {ve}")
                raise

    except Exception as e:
        logger.error(f"Error loading wallet data: {str(e)}")
        raise

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "https://nema-frontend.fly.dev",
                "https://nema.ac"
            ]
        }
    })

    try:
        # Load wallet data when app starts
        load_wallet_data()
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        # You might want to decide whether to raise this error or continue with empty wallet_data
        wallet_data = {}

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
