# WeatherForecastCLI
This repository contains a Python-based command-line tool for fetching and displaying the current weather forecast for any city. It leverages the OpenWeatherMap API to fetch weather data.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone this repository using git:

    ```bash
    git clone https://github.com/your_username/WeatherForecastCLI.git
    cd WeatherForecastCLI
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your OpenWeatherMap API key:

    ```bash
    API_KEY=your_api_key_here
    ```

## Usage
You can run the weather forecast tool using the following command:

```bash
python forecast.py 'City Name'
```

For example, to get the forecast for New York, you would run:

```bash
python forecast.py 'New York'
```

By default, the country is set to 'us'. If you want to get the forecast for a city in a different country, use the --country flag:

```bash
python forecast.py 'London' --country 'uk'
```