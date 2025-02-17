from flask import Flask
import csv
import os

# Global variable to store wallet data
wallet_data = {}

def load_wallet_data():
    global wallet_data
    csv_path = os.path.join('static', 'drop', 'wallets.csv')
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            # Assuming CSV has 'wallet' and 'balance' columns
            wallet_data = {row['wallet']: row['balance'] for row in reader}
    except Exception as e:
        print(f"Error loading wallet data: {e}")
        wallet_data = {}

def create_app():
    app = Flask(__name__)
    
    # Load wallet data when app starts
    load_wallet_data()
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app
