# app/routes.py
from flask import Blueprint, jsonify
from . import wallet_data, logger

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message='Hello, World!')

@main.route('/check-wallet/<wallet_id>')
def check_wallet(wallet_id: str):
    try:
        if not wallet_id:
            logger.warning("Empty wallet ID provided")
            return jsonify({'error': 'Wallet ID cannot be empty'}), 400
            
        exists = wallet_id in wallet_data
        projected_amount = wallet_data.get(wallet_id, {}).get('projected_amount', 0) if exists else 0
        
        # for now multiply by .9 to account for historical holders claiming %
        projected_amount = projected_amount * 0.9
        projected_amount = round(projected_amount, 2)
        
        logger.info(f"Wallet check - ID: {wallet_id}, Exists: {exists}, Projected Amount: {projected_amount}")
        
        return jsonify({'exists': exists, 'projected_amount': projected_amount})
        
    except Exception as e:
        logger.error(f"Error checking wallet {wallet_id}: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@main.route('/healthz')
def health_check():
    return jsonify({'status': 'healthy'}), 200
