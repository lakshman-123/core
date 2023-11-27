import pytest
from unittest.mock import MagicMock, patch
from homeassistant.components.open_meteo.weather import OpenMeteoWeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

@pytest.fixture
def mock_open_meteo_entity():
    """Fixture to create a mock OpenMeteoWeatherEntity."""
    mock_entry = MagicMock(spec=ConfigEntry)
    mock_coordinator = MagicMock(spec=DataUpdateCoordinator)

    # Setting up the 'data' attribute for the mock_coordinator
    mock_coordinator.data = MagicMock()
    mock_coordinator.data.current_weather = MagicMock(temperature=10, wind_speed=5)

    entity = OpenMeteoWeatherEntity(entry=mock_entry, coordinator=mock_coordinator)
    return entity


# ... rest of your code ...


def calculate_expected_wind_chill(temperature, wind_speed):
    """Helper function to calculate expected wind chill."""
    return 13.12 + 0.6215 * temperature - 11.37 * pow(wind_speed, 0.16) + 0.3965 * temperature * pow(wind_speed, 0.16)

def test_wind_chill_calculation(mock_open_meteo_entity):
    """Test if the wind chill calculation is correct."""
    # Setup test data
    test_temperature = 10  # Example temperature in Celsius
    test_wind_speed = 5   # Example wind speed in km/h

    # Setting mock data
    mock_open_meteo_entity.coordinator.data.current_weather.temperature = test_temperature
    mock_open_meteo_entity.coordinator.data.current_weather.wind_speed = test_wind_speed

    # Expected wind chill calculated by the helper function
    expected_wind_chill = calculate_expected_wind_chill(test_temperature, test_wind_speed)

    # Actual wind chill calculated by the entity
    actual_wind_chill = mock_open_meteo_entity.wind_chill

    # Asserting that the actual wind chill matches the expected value
    assert actual_wind_chill == pytest.approx(expected_wind_chill)


