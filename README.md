# Nema API
Flask API for Nema wallet linking and verification.

## Prerequisites
- Python 3.13 or higher
- Poetry (Python package manager)

## Installation

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd api
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Running the Application

1. Start the development server:
   ```bash
   poetry run python run.py
   ```

   The server will start on `http://localhost:8080`

## Project Structure

```

## API Endpoints

- `GET /`: Health check endpoint
- `GET /healthz`: Health check endpoint
- `GET /check-wallet/<wallet_id>`: Check if a wallet exists and get projected amount
- `POST /link-wallet`: Link Solana and Ethereum wallets
- `GET /check-link/<solana_address>`: Check if a Solana wallet is linked

## Development

To add new dependencies:
```bash
poetry add package-name
```

To update dependencies:
```bash
poetry update
```

## Database
The application uses SQLite for storing wallet linking information. The database file (`wallet_data.db`) is created automatically on first run.

## Environment Variables
No environment variables are required for basic operation. The application uses default configurations.
