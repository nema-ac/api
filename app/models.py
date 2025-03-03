from . import db
from datetime import datetime

class WalletLink(db.Model):
    __tablename__ = 'wallet_links'

    solana_address = db.Column(db.String, primary_key=True)
    eth_address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<WalletLink {self.solana_address} -> {self.eth_address}>'

    def to_dict(self):
        return {
            'solana_address': self.solana_address,
            'eth_address': self.eth_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
