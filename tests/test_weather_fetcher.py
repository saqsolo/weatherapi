import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import Mock, patch
from weather_fetcher import WeatherDataFetcher
import weatherapi

@pytest.fixture
def mock_weather_response():
    mock_condition = Mock()
    mock_condition.text = "Partly cloudy"
    
    mock_current = Mock()
    mock_current.temp_c = 20.0
    mock_current.temp_f = 68.0
    mock_current.humidity = 65
    mock_current.wind_kph = 15.5
    mock_current.wind_degree = 180
    mock_current.wind_dir = "S"
    mock_current.pressure_mb = 1015.0
    mock_current.precip_mm = 0.0
    mock_current.cloud = 25
    mock_current.feelslike_c = 19.5
    mock_current.condition = mock_condition
    
    mock_response = Mock()
    mock_response.current = mock_current
    return mock_response

@pytest.fixture
def weather_fetcher():
    return WeatherDataFetcher(
        api_key="test_key",
        cities=["London,UK", "Paris,FR"],
        db_connection_string="sqlite:///:memory:"
    )

@pytest.fixture
def mock_weather_api():
    with patch('weatherapi.Configuration') as mock:
        yield mock

def test_init(mock_weather_api):
    fetcher = WeatherDataFetcher(
        api_key='test_key',
        cities=['London,UK'],
        db_connection_string='sqlite:///:memory:'
    )
    assert fetcher.configuration.api_key['key'] == 'test_key'

@patch('weatherapi.APIsApi.realtime_weather')
def test_fetch_weather_data(mock_realtime_weather, weather_fetcher, mock_weather_response):
    # Configure mock to return our mock response
    mock_realtime_weather.return_value = mock_weather_response
    
    # Call the method
    df = weather_fetcher.fetch_weather_data()
    
    # Verify the result
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2  # Two cities
    assert list(df.columns) == [
        'city', 'timestamp', 'temperature_c', 'temperature_f', 'humidity',
        'wind_kph', 'wind_degree', 'wind_dir', 'pressure_mb', 'precip_mm',
        'cloud', 'feels_like_c', 'condition'
    ]
    
    # Check values
    assert df.iloc[0]['temperature_c'] == 20.0
    assert df.iloc[0]['condition'] == "Partly cloudy"

@patch('weatherapi.APIsApi.realtime_weather')
def test_fetch_weather_data_with_error(mock_realtime_weather, weather_fetcher, mock_weather_response):
    # Add mock_weather_response parameter and configure mocks
    mock_realtime_weather.side_effect = [
        Exception("API Error"),
        mock_weather_response
    ]
    
    # Call the method
    df = weather_fetcher.fetch_weather_data()
    
    # Verify that we still get data for the second city
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1  # Only one city succeeded

@patch('weather_fetcher.WeatherDataFetcher.fetch_weather_data')
def test_update_database(mock_fetch, weather_fetcher):
    # Create a sample DataFrame
    sample_data = pd.DataFrame({
        'city': ['London,UK'],
        'timestamp': [datetime.now()],
        'temperature_c': [20.0],
        'temperature_f': [68.0],
        'humidity': [65],
        'wind_kph': [15.5],
        'wind_degree': [180],
        'wind_dir': ['S'],
        'pressure_mb': [1015.0],
        'precip_mm': [0.0],
        'cloud': [25],
        'feels_like_c': [19.5],
        'condition': ['Partly cloudy']
    })
    
    mock_fetch.return_value = sample_data
    
    # Call the method
    weather_fetcher.update_database()
    
    # Verify the data was written to the database
    result = pd.read_sql('SELECT * FROM weather_data', weather_fetcher.engine)
    assert len(result) == 1
    assert result.iloc[0]['city'] == 'London,UK' 