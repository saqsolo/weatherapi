import os
from dotenv import load_dotenv

# Load environment variables from .env file


import time
from weather_fetcher import WeatherDataFetcher

load_dotenv()
# Configuration from environment variables
API_KEY = os.getenv('WEATHER_API_KEY','e6192bc9ac9b441db63203714240712')
#if not API_KEY:
#    raise ValueError("WEATHER_API_KEY environment variable is required")

CITIES = [
    'London,UK',
    'New York,US',
    'Tokyo,JP',
    'Sydney,AU',
    'Paris,FR'
]

# Get database connection string from environment
DB_CONNECTION = os.getenv('DB_CONNECTION', 'postgresql://weather_user:weather_password@postgres:5432/weather_db')

# Update interval in seconds (5 minutes)
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', '300'))

def main():
    fetcher = WeatherDataFetcher(
        api_key=API_KEY,
        cities=CITIES,
        db_connection_string=DB_CONNECTION
    )
    
    while True:
        fetcher.update_database()
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main() 