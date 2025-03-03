# app/routes.py
import base64

from flask import Blueprint, jsonify, request
from solders.pubkey import Pubkey
from solders.signature import Signature

from . import logger, wallet_data
from .db import get_linked_wallet_from_sol

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message='Hello, World!')

@main.route('/healthz')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@main.route('/check-wallet/<wallet_id>', methods=['GET'])
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


@main.route('/link-wallet', methods=['POST'])
def link_wallet():
    data = request.json

    solana_address = data.get('solanaAddress')
    eth_address = data.get('ethAddress')
    signature_b64 = data.get('signature')
    
    if not all([solana_address, eth_address, signature_b64]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    if solana_address not in wallet_data:
        return jsonify({"success": False,"message": "Solana wallet is not eligible for airdrop" }), 400
        
    try:
        # Convert base64 signature to bytes
        signature_bytes = base64.b64decode(signature_b64)

        # Get the public key object
        public_key = Pubkey.from_string(solana_address)

        # Convert message to bytes
        message_bytes = message.encode('utf-8')
        
        try:
            signature = Signature.from_bytes(signature_bytes)
            is_valid = signature.verify(public_key, message_bytes)
        except Exception as sig_error:
            logger.error(f"Signature verification error: {str(sig_error)}")
            is_valid = False

        if not is_valid:
            return jsonify({"success": False, "message": "Invalid signature"}), 400

    except Exception as e:
        logger.error(f"Error verifying signature: {str(e)}")
        return jsonify({"success": False,"message": "An error occurred while processing your request"}), 500


@main.route('/check-link/<solana_address>', methods=['GET'])
def check_link(solana_address: str):
    try:
        eth_wallet = get_linked_wallet_from_sol(solana_address)

        if eth_wallet:
            return jsonify({ "linked": True, "eth_address": eth_wallet })
        else:
            return jsonify({ "linked": False })

    except Exception as e:
        logger.error(f"Error checking link for {solana_address}: {str(e)}")
        return jsonify({"success": False,"message": "An error occurred while checking the link"}), 500