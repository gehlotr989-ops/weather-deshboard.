import requests


def validate_city_name(city: str) -> str:
  """Validates that the city name is not empty and contains valid characters."""
  if not city or not city.strip():
    raise ValueError("City name cannot be empty.")

  cleaned_city = city.strip()
  if not all(c.isalpha() or c.isspace() or c in "-'" for c in cleaned_city):
    raise ValueError(
        "City name contains invalid characters. Use letters and spaces only."
    )

  return cleaned_city


def fetch_weather_data(city: str, api_key: str = None) -> dict:
  """Fetches weather data from the OpenWeatherMap API with error handling."""
  # Using a mock fallback mechanism if API key is not provided so the app runs out-of-the-box,
  # or you can plug in your real OpenWeatherMap API key.
  if not api_key or api_key == "YOUR_API_KEY_HERE":
    # Fallback simulated data for testing/demonstration if no API key is set
    return _get_mock_weather_data(city)

  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

  try:
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
      raise LookupError(f"City '{city}' not found. Please check the spelling.")
    elif response.status_code == 401:
      raise PermissionError("Invalid API Key. Please check your credentials.")

    response.raise_for_status()
    return response.json()

  except requests.exceptions.ConnectionError:
    raise ConnectionError(
        "Failed to connect to the weather service. Check your internet"
        " connection."
    )
  except requests.exceptions.Timeout:
    raise TimeoutError(
        "The request timed out. Please try again later."
    )


def _get_mock_weather_data(city: str) -> dict:
  """Provides simulated data if no live API key is configured."""
  return {
      "name": city.capitalize(),
      "main": {"temp": 24.5, "humidity": 65, "pressure": 1012},
      "weather": [{"description": "scattered clouds"}],
      "wind": {"speed": 4.1},
  }