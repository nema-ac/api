# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Only use debug mode when running locally
    app.run(host="0.0.0.0", port=8080)
