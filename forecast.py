
import sys
import argparse
import requests
from termcolor import colored
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

# Load environment variables from .env file
if not load_dotenv(path.join(basedir, ".env")):
    print(colored("Error: .env file not found. Please create one with your API key.", 'red'))
    sys.exit(1)

# Load the API key from environment variables
API_KEY = environ.get("API_KEY")
if not API_KEY:
    print(colored("Error: API_KEY not found in .env file. Please add your OpenWeatherMap API key.", 'red'))
    sys.exit(1)

GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# This function fetches the latitude and longitude of a given city
def get_coordinates(city, country):
    """
    Fetches the latitude and longitude of a given city using OpenWeatherMap API.
        :param city: The name of the city.
        :param country: The country code of the city.
        :return: A tuple containing the latitude and longitude of the city, or None if not found.
    """
    try:
        params = {'q': city + ',' + country, 'limit': 1, 'appid': API_KEY}
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(colored(f'Error: City {city} not found.', 'red'))
        elif response.status_code == 401:
            print(colored(f'Error: Invalid API key', 'red'))
        else:
            print(colored('Error: ', 'red'), err)
    except requests.exceptions.RequestException as err:
        print(colored('Error: ', 'red'), err)
    except Exception as err:
        print(colored('Error: ', 'red'), err)
    else:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            print(colored(f'Error: Unable to fetch coordinates for city {city}.', 'red'))

# This function fetches a weather forecast for a location specified by its latitude and longitude
def get_forecast(lat, lon):
    """
    Fetches a weather forecast for a location specified by its latitude and longitude using OpenWeatherMap API.
        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :return: A JSON object containing the forecast data or None if not found.
    """
    try:
        params = {
            'lat': lat, 
            'lon': lon,
            'appid': API_KEY,
            'units': 'imperial',
            'lang': 'en'
        }
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(colored(f'Error: Unable to fetch forecast data for coordinates lat:{lat} lon:{lon}', 'red'))
        elif response.status_code == 401:
            print(colored(f'Error: Invalid API key', 'red'))
        else:
            print(colored('Error: ', 'red'), err)
    except requests.exceptions.RequestException as err:
        print(colored('Error: ', 'red'), err)
    except Exception as err:
        print(colored('Error: ', 'red'), err)
    else:
        data = response.json()
        if 'list' in data:
            return data
        else:
            print(colored(f'Error: Unable to fetch forecast data for coordinates lat:{lat} lon:{lon}', 'red'))

# This function prints a weather forecast in a user-friendly format
def print_weather(city, country, data):
    # Print the location
    # For each forecast in the data, print the time, temperature, and weather description
    # Catch and handle any exceptions that might occur during this process
    try:
        print(colored('Current weather forecast for {}, {}:'.format(city, country), 'cyan'))
        for forecast in data['list']:
            time = colored(forecast['dt_txt'], 'yellow')
            temp = colored(forecast['main']['temp'], 'green')
            desc = colored(forecast['weather'][0]['description'], 'blue')
            print('\t{}: {} degrees F, {}'.format(time, temp, desc))
    except KeyError as err:
        print(colored('Error: ', 'red'), err)
    except Exception as err:
        print(colored('Error: ', 'red'), err)

def main():
    # Parse command line arguments using argparse
    parser = argparse.ArgumentParser(description="Get the current weather information for a city")
    parser.add_argument('city', help='City to get forecast for')
    parser.add_argument('--country', default='us', help='2-letter country code of the city to get forecast for (default: "us")')

    # If a city name was provided, fetch and print a weather forecast for it
    # Otherwise, print an error message and exit
    try:
        args = parser.parse_args()
    except SystemExit:
        print(colored("Error: Invalid command. You must provide a city name. Example: ", 'red') + colored("python forecast.py 'New York'", 'yellow'))
        sys.exit(1)

    # Get coordinates for the city and fetch and print the weather data
    coordinates = get_coordinates(args.city, args.country)
    if coordinates:
        forecast_data = get_forecast(*coordinates)
        if forecast_data:
            print_weather(args.city, args.country, forecast_data)

# This is the main entry point of the script
if __name__ == '__main__':
    main()