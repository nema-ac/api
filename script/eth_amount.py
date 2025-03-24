import csv
import os


def calculate_total_eth():
    # Get the absolute paths for the CSV files
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wallets_path = os.path.join(base_dir, 'static', 'drop', 'wallets.csv')
    sol_eth_path = os.path.join(base_dir, 'static', 'drop', 'sol_eth_wallet.csv')
    print(wallets_path)
    print(sol_eth_path)
    
    # Create a dictionary to store wallet balances
    wallet_balances = {}
    
    # Read wallets.csv to get balances
    with open(wallets_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wallet_balances[row['wallet']] = int(row['balance'])
    
    # Read sol_eth_wallet.csv and map eth wallets
    total_balance = 0
    eth_balances = {}
    
    with open(sol_eth_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sol_wallet = row['sol_wallet']
            eth_wallet = row['eth_wallet']
            balance = wallet_balances.get(sol_wallet, 0)
            eth_balances[sol_wallet] = {
                'eth_wallet': eth_wallet,
                'balance': balance
            }
            total_balance += balance
    
    # Print results
    print(f"Total claimed WORM tokens: {total_balance}")
    
    # Calculate the airdrop and team wallet amounts
    total_worm_supply = 1_000_000_000
    total_nema_supply = 1_000_000_000
    airdrop_percentage = .6
    team_wallet_percent = .1
    
    claimed_percent = airdrop_percentage * total_balance / total_worm_supply
    claimed_amount = claimed_percent * total_nema_supply
    
    team_wallet_amount = round(team_wallet_percent * total_nema_supply + ((airdrop_percentage * total_nema_supply) - claimed_amount))
    print(f"Airdrop Percent:     {claimed_percent:.2%}, Total: {claimed_amount:,}")
    print(f"Team Wallet Percent: {(team_wallet_amount / total_nema_supply):.2%}, Total: {team_wallet_amount:,}")
    
    # We want to inflate the claimed percent to be 35% from whatever it is
    factor = .35 / claimed_percent
    print(f"Factor: {factor:.2f}")
    
    
    # Write mapped_nema_airdrop to a CSV file in the form:
    # sol_wallet, eth_wallet, worm_balance, nema_balance
    factoredTotal = 0
    with open('./static/drop/mapped_nema_airdrop_35.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sol_wallet', 'eth_wallet', 'worm_balance', 'nema_balance'])
        for sol_wallet, data in eth_balances.items():
            writer.writerow([sol_wallet, data['eth_wallet'], data['balance'], round(data['balance']*0.6*factor)])
            factoredTotal += round(data['balance']*0.6*factor)
    print(f"Factored Total: {factoredTotal:,}")


if __name__ == "__main__":
    calculate_total_eth()
