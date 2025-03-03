import os
import sqlite3
from datetime import datetime

from flask import g

from . import logger

DATABASE = os.getenv('DATABASE_URL', 'wallet_data.db')
CLEAN_SLATE = os.getenv('CLEAN_SLATE', 'false').lower() == 'true'

def get_db():
    if 'db' not in g:
        logger.info(f"Connecting to database: {DATABASE}")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    try:
        with app.app_context():
            db = get_db()
            if CLEAN_SLATE:
                db.execute('DROP TABLE IF EXISTS sol_eth_wallets')
                db.commit()
                logger.info("Database dropped and recreated")
            
            # Create tables
            db.execute('''
                CREATE TABLE IF NOT EXISTS sol_eth_wallets (
                    sol_wallet TEXT PRIMARY KEY,
                    eth_wallet TEXT NOT NULL,
                    linked_at TEXT NOT NULL
                )
            ''')
            
            db.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_linked_wallet_from_sol(sol_wallet: str) -> str | None:
    """
    Get the Ethereum wallet address for a given Solana wallet address.
    """
    try:
        db = get_db()
        cursor = db.cursor()  # Create a cursor
        cursor.execute('SELECT eth_wallet FROM sol_eth_wallets WHERE sol_wallet = ?', (sol_wallet,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting linked wallet from sol: {str(e)}")
        raise

def link_sol_eth_wallet(sol_wallet: str, eth_wallet: str) -> None:
    try:
        db = get_db()
        cursor = db.cursor()  # Create a cursor
        cursor.executemany(
            'INSERT OR REPLACE INTO sol_eth_wallets (sol_wallet, eth_wallet, linked_at) VALUES (?, ?, ?)',
            [(sol_wallet, eth_wallet, datetime.now().isoformat())]
        )
        db.commit()
        logger.info(f"Linked {sol_wallet} <-> {eth_wallet} in database")
    except Exception as e:
        logger.error(f"Error linking wallets: {str(e)}")
        raise 
    