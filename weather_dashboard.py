from utils import fetch_weather_data, validate_city_name


def process_weather_data(raw_data: dict) -> dict:
  """Processes and extracts key metrics from raw API response data."""
  try:
    processed = {
        "city": raw_data.get("name", "Unknown"),
        "temperature": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        "pressure": raw_data["main"]["pressure"],
        "description": raw_data["weather"][0]["description"].capitalize(),
        "wind_speed": raw_data["wind"]["speed"],
    }
    return processed
  except KeyError as e:
    raise ValueError(f"Error processing weather data structure: missing {e}")


def display_dashboard(data: dict):
  """Displays the formatted weather dashboard output."""
  print("\n" + "=" * 40)
  print(f"       WEATHER DASHBOARD: {data['city']}")
  print("=" * 40)
  print(f"  Temperature : {data['temperature']} °C")
  print(f"  Condition   : {data['description']}")
  print(f"  Humidity    : {data['humidity']}%")
  print(f"  Pressure    : {data['pressure']} hPa")
  print(f"  Wind Speed  : {data['wind_speed']} m/s")
  print("=" * 40 + "\n")


def main():
  print("Welcome to the Python Weather Dashboard Virtual Internship Project!")
  print(
      "(Note: You can use it right away with mock data or configure an"
      " OpenWeatherMap API key)\n"
  )

  api_key = input(
      "Enter your OpenWeatherMap API Key (press Enter to use demo mode): "
  ).strip()
  if not api_key:
    api_key = "YOUR_API_KEY_HERE"

  while True:
    try:
      user_input = input(
          "Enter city name to check weather (or type 'exit' to quit): "
      )
      if user_input.lower() == "exit":
        print("Exiting Weather Dashboard. Goodbye!")
        break

      # Step 1: Input Validation
      validated_city = validate_city_name(user_input)

      # Step 2: Data Fetching (with error handling)
      print(f"Fetching weather data for {validated_city}...")
      raw_data = fetch_weather_data(validated_city, api_key)

      # Step 3: Data Processing
      processed_data = process_weather_data(raw_data)

      # Step 4: Display Output
      display_dashboard(processed_data)

    except (ValueError, LookupError, ConnectionError, TimeoutError) as e:
      print(f"\n[Error] {e}\nPlease try again.\n")
    except Exception as e:
      print(f"\n[Unexpected Error] An unexpected error occurred: {e}\n")


if __name__ == "__main__":
  main()