import os
import time
import pandas as pd
from datetime import datetime
import weatherapi
from sqlalchemy import create_engine
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeatherDataFetcher:
    def __init__(self, api_key, cities, db_connection_string):
        self.configuration = weatherapi.Configuration()
        self.configuration.api_key['key'] = api_key
        self.api_instance = weatherapi.APIsApi(weatherapi.ApiClient(self.configuration))
        self.cities = cities
        self.engine = create_engine(db_connection_string)
        
    def fetch_weather_data(self):
        weather_data = []
        
        for city in self.cities:
            try:
                # Fetch current weather
                response = self.api_instance.realtime_weather(q=city)
                
                # Convert response to dictionary if it isn't already
                if not isinstance(response, dict):
                    response = response.to_dict()
                
                # Extract location and current data from dictionary
                location = response['location']
                current = response['current']
                condition = current['condition']
                
                data = {
                    # Location details
                    'city': location['name'],
                    'region': location['region'],
                    'country': location['country'],
                    'latitude': location['lat'],
                    'longitude': location['lon'],
                    'timezone': location['tz_id'],
                    'local_time': location['localtime'],
                    
                    # Current weather details
                    'timestamp': datetime.now(),
                    'last_updated': current['last_updated'],
                    'temperature_c': current['temp_c'],
                    'temperature_f': current['temp_f'],
                    'is_day': current['is_day'],
                    'condition': condition['text'],
                    'condition_icon': condition['icon'],
                    'condition_code': condition['code'],
                    
                    # Wind information
                    'wind_mph': current['wind_mph'],
                    'wind_kph': current['wind_kph'],
                    'wind_degree': current['wind_degree'],
                    'wind_dir': current['wind_dir'],
                    'gust_mph': current['gust_mph'],
                    'gust_kph': current['gust_kph'],
                    
                    # Atmospheric conditions
                    'pressure_mb': current['pressure_mb'],
                    'pressure_in': current['pressure_in'],
                    'precip_mm': current['precip_mm'],
                    'precip_in': current['precip_in'],
                    'humidity': current['humidity'],
                    'cloud': current['cloud'],
                    
                    # Comfort metrics
                    'feels_like_c': current['feelslike_c'],
                    'feels_like_f': current['feelslike_f'],
                    'windchill_c': current['windchill_c'],
                    'windchill_f': current['windchill_f'],
                    'heatindex_c': current['heatindex_c'],
                    'heatindex_f': current['heatindex_f'],
                    
                    # Visibility and other metrics
                    'dewpoint_c': current['dewpoint_c'],
                    'dewpoint_f': current['dewpoint_f'],
                    'vis_km': current['vis_km'],
                    'vis_miles': current['vis_miles'],
                    'uv': current['uv']
                }
                weather_data.append(data)
                logger.info(f"Successfully fetched weather data for {location['name']}, {location['country']}")
                
            except Exception as e:
                logger.error(f"Error fetching data for {city}: {str(e)}")
                continue
        
        return pd.DataFrame(weather_data)
    
    def update_database(self):
        try:
            df = self.fetch_weather_data()
            df.to_sql('weather_data', self.engine, if_exists='append', index=False)
            logger.info(f"Successfully updated weather data for {len(df)} cities")
        except Exception as e:
            logger.error(f"Error updating database: {str(e)}") 