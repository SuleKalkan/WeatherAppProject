WeatherAppProject Developed by Sule Kalkan
August 16, 2025


# WeatherAPP Project
A weather application built with Python and PyQt5

## Description: 
This application gathers the current and 5-day forecast weather data by using **OpenWeatherMap API**. The app also allows users to create, read, update, and delete weather records from SQLite database that came (built-in) with  Python.

## Features:
- Allows users to search for weather by typing EITHER 'City Name' or 'Zip Code'
- Result Displays:
   - The current tempeture in Fahrenheit
   - Weather Emoji such as: '🔆','☁️', '🌪️', etc...
   - Weather description
   - 5-day forecast
- Type weather data with a date range( start date, end date, weather record)
- Create a weather data
- Read the created data
- Update the created data
- delete any weather data from the record.
  - for the delete function to work: User must type in the exact start date, end date and weather data to delete it.


## How My Code Works:

1. The User Interface (built with PyQt5)
  - The Interface is created with **QLabel**, **QLineEdit**, **QScrollArea**, and **QPushButton**
  - This allows users to type in a city name or a zip code to gather weather data
  - The buttons on the application are connected to functions that manages weather related tasks such as **display_weather'**, **get_weather_icon**, **create_WRecord**, etc...

2. Weather search and data gathering
  - Function: **def weather_result(self)**
  - I used an API key from **OpenWeatherMap API** that helps me gather my weather data for my application.
  - This API retrieves:
     - Current temperature in Kelvin, but I converted to Fahrenheit
     - Weather descriptions
     - Weather ID to determine the Weather emoji. We can see this in the **def get_weather_icon(weather_id)** function, that certain numbers/IDs determine the weather's description.

3. 5-Day weather forecast
  - Function: **def display_forecast(self, data)**
  - This function loops through the provided forecast data and only selects the Mid-day values (12:00 pm)
  - Also displays the date, temp in F°, description, and weather emoji.

4. The Database (SQLite3)
  - I didn't need an additional installation, since Python came with sqlite3 module that allowed me to use SQLite.
    - **import sqlite3**
  - A Table (weather_records) is created with the **self.cursor.execute(...)**
  - How it works:
    - **create_WRecord()** function: user inserts a weather data by typing start date, end date, and weatehr record (such as sunny, rainy, or anything specific)
    - **read_WRecord()** function: Allows users to read through the weather data they created. This can be done by scrolling through the records.
       - When reading the records, the weather results are displayed in a little scroallable box-like area (made with **QScrollArea**). But this box replaces the current weather's temperature display.
    - **update_WRecord()** function: Updates the existing weather record.
    - **delete_WRecord()** function: Deletes records typed by users that are specific.

5. Error cases and how the code handles it
  - The application manages and checks for network issues, invalid inputs, API related errors, missing city name or zip codes.
  - Functions that manages errors:
     - **def weather_result(self)**
         - Checks for city name and zip code related errors
         - Checks for all API related requests such as HTTP errors( 400,401, 404, 500, 502, etc...), which checks for invalid API key, connection errors, gateway timeouts, etc...
    - **def display_error(self, message)**
        - Displays the error message in the interface when an error is found.
    - Other functions such as **create_WRecord(), validate_date(), update_WRecord(), and delete_WRecord()** also checks for errors in their own fields. 

## How to run the code

1. Clone the repository on Github:
   - git clone https://github.com/SuleKalkan/WeatherAppProject.git
   - cd WeatherAppProject

2. Install required items:
   - pip install PyQt5 requests

3. Inserting your own OpenWeatherMap API key:
   - Open the file WeatherAppProject.py in VS Code
   - Locate this line on my code:
      - api_key = "4981db413db6be52cb48f5ea063549a6"
   - replace the "4981db413db6be52cb48f5ea063549a6" with your own API key inside the quotations

4. Run the application
   - Click on the Run OR:
   - Click on Terminal --> new Terminal and paste the following: python main.py
    
         


