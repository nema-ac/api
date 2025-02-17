# app/routes.py
from flask import Blueprint, jsonify
from . import wallet_data

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message='Hello, World!')

@main.route('/check-wallet/<wallet_id>')
def check_wallet(wallet_id):
    exists = wallet_id in wallet_data
    return jsonify(exists=exists)
