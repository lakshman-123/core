from homeassistant.components.weather import WeatherEntity
from homeassistant.const import (
    TEMP_CELSIUS,
    SPEED_KILOMETERS_PER_HOUR,
    LENGTH_MILLIMETERS,
)
from homeassistant.util import dt as dt_util
from open_meteo import Forecast as OpenMeteoForecast
from unittest.mock import Mock

# Import DOMAIN from your component's const.py file
from homeassistant.components.open_meteo.const import DOMAIN
from homeassistant.components.open_meteo.weather import OpenMeteoWeatherEntity


async def test_open_meteo_entity_properties():
    """Test the OpenMeteo weather entity properties."""
    entry = Mock()
    coordinator = Mock()
    coordinator.data = OpenMeteoForecast()
    coordinator.data.current_weather = Mock()
    coordinator.data.current_weather.weather_code = "clear-night"
    coordinator.data.current_weather.temperature = 20.5
    coordinator.data.current_weather.wind_speed = 5.0
    coordinator.data.current_weather.wind_direction = 180

    entity = OpenMeteoWeatherEntity(entry=entry, coordinator=coordinator)

    assert entity.name is None
    assert entity.unique_id == entry.entry_id
    assert entity.device_info.manufacturer == "Open-Meteo"
    assert entity.device_info.name == entry.title
    assert entity.device_info.identifiers == {(DOMAIN, entry.entry_id)}

    assert entity.condition == "clear-night"
    assert entity.native_temperature == 20.5
    assert entity.native_temperature_unit == TEMP_CELSIUS
    assert entity.native_wind_speed == 5.0
    assert entity.native_wind_speed_unit == SPEED_KILOMETERS_PER_HOUR
    assert entity.wind_bearing == 180


async def test_open_meteo_entity_forecast():
    """Test the OpenMeteo weather entity forecast."""
    entry = Mock()
    coordinator = Mock()
    coordinator.data = OpenMeteoForecast()
    coordinator.data.daily = Mock()
    coordinator.data.daily.time = [dt_util.now(), dt_util.now()]
    coordinator.data.daily.weathercode = ["clear-day", "partly-cloudy-day"]
    coordinator.data.daily.precipitation_sum = [0.0, 2.5]
    coordinator.data.daily.temperature_2m_max = [25.0, 20.0]
    coordinator.data.daily.temperature_2m_min = [15.0, 10.0]
    coordinator.data.daily.wind_direction_10m_dominant = [180, 270]
    coordinator.data.daily.wind_speed_10m_max = [10.0, 15.0]

    entity = OpenMeteoWeatherEntity(entry=entry, coordinator=coordinator)
    forecasts = entity.forecast

    assert len(forecasts) == 2

    forecast_today = forecasts[0]
    assert forecast_today.datetime is not None
    assert forecast_today.condition == "clear-day"
    assert forecast_today.native_precipitation == 0.0
    assert forecast_today.native_precipitation_unit == LENGTH_MILLIMETERS
    assert forecast_today.native_temperature == 25.0
    assert forecast_today.native_temperature_unit == TEMP_CELSIUS
    assert forecast_today.native_templow == 15.0
    assert forecast_today.wind_bearing == 180
    assert forecast_today.native_wind_speed == 10.0
    assert forecast_today.native_wind_speed_unit == SPEED_KILOMETERS_PER_HOUR
