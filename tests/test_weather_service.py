import pytest
import os
from dotenv import load_dotenv
from unittest.mock import patch, Mock
from importlib import reload
import weather_service

# Load environment variables at the start of tests
load_dotenv()

@pytest.fixture(autouse=True)
def clear_env():
    """Clear environment variables before each test"""
    original_environ = dict(os.environ)
    os.environ.clear()
    yield
    print(f'inside clear_env = {os.getenv('WEATHER_API_KEY')}')
    os.environ.update(original_environ)

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        'WEATHER_API_KEY': 'test_key',
        'DB_CONNECTION': 'sqlite:///:memory:',
        'UPDATE_INTERVAL': '60'
    }):
        yield

def test_config_validation():
    print(f'inside test_config_validation before return value = {os.getenv('WEATHER_API_KEY')}')
    # Clear all environment variables and ensure load_dotenv returns None
    
    print(f'inside test_config_validation after return value = {os.getenv('WEATHER_API_KEY')}')
    # Use clear=True to ensure environment is completely cleared
    with patch.dict('os.environ', {}, clear=True):
        print(f'inside test_config_validation after clearing patch = {os.getenv('WEATHER_API_KEY')}')
        # Force reload of weather_service to trigger the config validation
        with pytest.raises(ValueError, match="WEATHER_API_KEY environment variable is required"):
            print(f'inside test_config_validation before reloading = {os.getenv('WEATHER_API_KEY')}')
            reload(weather_service)
            print(f'inside test_config_validation after reloading = {os.getenv('WEATHER_API_KEY')}')

def test_update_interval_parsing():
    with patch.dict(os.environ, {
        'WEATHER_API_KEY': 'test_key',
        'UPDATE_INTERVAL': '60'
    }):
        reload(weather_service)
        assert weather_service.UPDATE_INTERVAL == 60

@patch('weather_service.WeatherDataFetcher')
@patch('time.sleep', side_effect=InterruptedError)
def test_main_loop(mock_sleep, mock_fetcher_class, mock_env_vars):
    mock_fetcher = Mock()
    mock_fetcher_class.return_value = mock_fetcher
    
    with pytest.raises(InterruptedError):
        weather_service.main()
    
    mock_fetcher_class.assert_called_once()
    mock_fetcher.update_database.assert_called_once() 