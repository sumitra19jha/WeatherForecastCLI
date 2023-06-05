
import sys
import argparse
import requests
from termcolor import colored
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

# [Copilot] Check if the .env file exists in the basedir. If not, print an error message in red and exit the program.
if not path.exists(path.join(basedir, '.env')):
    print(colored("Error: .env file not found. Please create a .env file in the base directory.", 'red'))
    sys.exit(1)

load_dotenv(path.join(basedir, ".env"))
API_KEY = environ.get("API_KEY")

# [Copilot] If API_KEY is not found, print an error message in red and exit the program.
if not API_KEY:
    print(colored("Error: API_KEY not found in .env file. Please add your OpenWeatherMap API key.", 'red'))
    sys.exit(1)

GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# This function fetches the latitude and longitude of a given city
def get_coordinates(city, country=None):
    """
    Fetches the latitude and longitude of a given city using OpenWeatherMap API.
        :param city: The name of the city.
        :param country: The country code of the city.
        :return: A tuple containing the latitude and longitude of the city, or None if not found.
    """
    try:
        if country:
            params = {'q': city + ',' + country, 'limit': 1, 'appid': API_KEY}
        else:
            params = {'q': city, 'limit': 1, 'appid': API_KEY}
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()
    # [Copilot] Handle all potential exceptions including HTTP errors, Request exceptions, and general exceptions. Provide user-friendly error messages for each case.
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
def get_forecast(city, lat, lon):
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
    # [Copilot] Handle all potential exceptions including HTTP errors, Request exceptions, and general exceptions. Provide user-friendly error messages for each case.
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
    # [Copilot] Handle all potential exceptions
    except KeyError as err:
        print(colored('Error: ', 'red'), err)
    except Exception as err:
        print(colored('Error: ', 'red'), err)

# [Copilot] Define the main function. Use argparse to parse command line arguments for a city and optionally a country. Validate the arguments, fetching coordinates and a weather forecast for the city if valid, else print an error and exit. If coordinates and forecast data are found, print the weather data.
def main():
    parser = argparse.ArgumentParser(description='Fetches and displays the weather forecast for a given location.')
    parser.add_argument('city', type=str, help='The name of the city')
    parser.add_argument('--country', type=str, help='The country code of the city')
    try:
        args = parser.parse_args()
        city = args.city
        country = args.country
    except SystemExit:
        print(colored("Error: Invalid command. You must provide a city name. Example: ", 'red') + colored("python forecast.py 'New York'", 'yellow'))
        sys.exit(1)

    coords = get_coordinates(city, country)
    if not coords:
        sys.exit(1)
    else:
        lat, lon = coords

    forecast = get_forecast(city, lat, lon)
    if not forecast:
        sys.exit(1)
    else:
        print_weather(city, country, forecast)

# This is the main entry point of the script
if __name__ == '__main__':
    main()