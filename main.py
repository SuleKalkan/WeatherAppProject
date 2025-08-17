import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QScrollArea
from datetime import datetime, timedelta

#This is the weatherApp class that takes in QWidget as a parameter.
#It creates labels, a scroll area, and defines button functions for the interface.

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        

        self.name_label = QLabel("Developed by Sule Kalkan", self)
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.zip_label = QLabel("Or Enter Zip Code: ", self)
        self.zip_input = QLineEdit(self)
        self.weather_button = QPushButton("Get Weather", self)

        self.result_label = QLabel(self)
        self.result_label.setWordWrap(True)
        self.scroll_a = QScrollArea(self)
        self.scroll_a.setWidgetResizable(True)
        self.scroll_a.setWidget(self.result_label)
        self.scroll_a.setFixedHeight(120)


        self.Image_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.forecast_label = QLabel(self)
        self.info_button = QPushButton("Info", self)

        self.conn = sqlite3.connect('weather.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT,
                start_date TEXT,
                end_date TEXT,
                weather_data TEXT
                date_time TEXT
    
            )
         """)
        self.conn.commit()
        
       
        self.start_date_label = QLabel("Start Date (YYYY-MM-DD):", self)
        self.start_date_input = QLineEdit(self)
        self.end_date_label = QLabel("End Date (YYYY-MM-DD):", self)
        self.end_date_input = QLineEdit(self)
        self.weather_data_label = QLabel("Weather Data:", self)
        self.weather_data_input = QLineEdit(self)

        self.create_button = QPushButton("Create Weather Record", self)
        self.read_button = QPushButton("Read Weather Records", self)
        self.update_button = QPushButton("Update Weather Record", self)
        self.delete_button = QPushButton("Delete Weather Record", self)


        self.initialUI()


    #This function builds the main UI of the app, it adds widgets/buttons to the interface, sets their alignments and styles such as font size and style.
    def initialUI(self):
        

        vbox = QVBoxLayout()
        
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.zip_label)
        vbox.addWidget(self.zip_input)
        vbox.addWidget(self.weather_button)
        
        vbox.addWidget(self.scroll_a)

        vbox.addWidget(self.Image_label)
        vbox.addWidget(self.desc_label)
        vbox.addWidget(self.forecast_label)

        

        vbox.addWidget(self.start_date_label)
        vbox.addWidget(self.start_date_input)
        vbox.addWidget(self.end_date_label)
        vbox.addWidget(self.end_date_input)
        vbox.addWidget(self.weather_data_label)
        vbox.addWidget(self.weather_data_input)
        vbox.addWidget(self.create_button)
        vbox.addWidget(self.read_button)
        vbox.addWidget(self.update_button)
        vbox.addWidget(self.delete_button)
        vbox.addWidget(self.info_button)

        

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.zip_label.setAlignment(Qt.AlignCenter)
        self.zip_input.setAlignment(Qt.AlignCenter)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.Image_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.zip_label.setObjectName("zip_label")
        self.zip_input.setObjectName("zip_input")
        self.weather_button.setObjectName("weather_button")
        self.result_label.setObjectName("Temp_label")
        self.Image_label.setObjectName("image_label")
        self.desc_label.setObjectName("description_label")
        

        self.setStyleSheet("""
                           
            QLabel#name_label {
                font-size: 20px;
                font-weight: bold;
            }
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label, QLabel#zip_label {
                font-size: 35px;
                font-weight: italic;
            }
            QLineEdit#city_input, QLineEdit#zip_input {
                font-size: 35px;
                
            }
            QPushButton#weather_button {
                font-size: 25px;
                font-weight: bold;
            }
            QLabel#Temp_label {
                font-size: 55px;
            }
            QLabel#image_label {
                font-size: 90px;
                font-faimily: "Segoe UI Emoji";
            }
            QLabel#description_label {
                font-size: 25px;
            }

                           
        """)

        self.weather_button.clicked.connect(self.weather_result)
        self.create_button.clicked.connect(self.make_create_record)
        self.read_button.clicked.connect(self.make_read_record)
        self.update_button.clicked.connect(self.make_update_record)
        self.delete_button.clicked.connect(self.make_delete_record)
        self.info_button.clicked.connect(self.show_info)


    #This function is called when the 'Get Weather' button is clicked. 
    #It gathers weather data from the OpenWeatherMap API based on the city name or zip code the user entered.
    #It handles HTTP errors and displays an error message if the request fails.
    def weather_result(self):
        api_key = "INSERT_YOUR_API_KEY"
        city = self.city_input.text().strip()
        zip_code = self.zip_input.text().strip()
        if zip_code:
           url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}"
           url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?zip={zip_code}&appid={api_key}"
        elif city:
           url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
           url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
        else:
            self.display_error("Please enter a city name or zip code.")
            return
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            res_forecast = requests.get(url_forecast)
            res_forecast.raise_for_status()
            data_forecast = res_forecast.json()

            if data["cod"] == 200 and data_forecast["cod"] == "200":
                self.display_weather(data)
                self.display_forecast(data_forecast)
        #These are the different HTTP errors that can be raised by the API request.
        except requests.exceptions.HTTPError as http_error:
            match res.status_code:
                case 400:
                    self.display_error("Invalid request. Please check the city name.")
                case 401:
                    self.display_error("Invalid API key.")
                case 403:
                    self.display_error("Access forbidden.")
                case 404:
                    self.display_error("City not found. Please check the city name.")   
                case 500:
                    self.display_error("Internal server error. Please try again later...")
                case 502:
                    self.display_error("Bad gateway. Please try again later...")
                case 503:
                    self.display_error("Service unavailable. Please try again later..")
                case 504:
                    self.display_error("Gateway timeout. Please try again later...")
                case _:
                    self.display_error(f"HTTP error.\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out. Please try again later...")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects. Please check the URL.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"A Request error occurred: {req_error}")
       
    #This function manages the display of the 5-day weather forecast.
    # it iterates through the weather data entries and extracts the Midday (12:00 PM) weather information for each day.
    def display_forecast(self, data):
        forecast_text = "<b> 5-day Forecast: </b><br>"
        shown_dates = set()
        for entry in data["list"]:
            dt_txt = entry["dt_txt"]
            date = dt_txt.split(" ")[0]
            hour = dt_txt.split(" ")[1][:2]
            if hour == "12" and date not in shown_dates:
                temp_kel = entry["main"]["temp"]
                temp_fah = (temp_kel * 9/5) - 459.67
                desc = entry["weather"][0]["description"]
                image = self.get_weather_icon(entry["weather"][0]["id"])
                forecast_text += f"{date}: {temp_fah:.0f}°F {image} {desc}<br>"
                shown_dates.add(date)
        self.forecast_label.setText(forecast_text)
        self.forecast_label.setStyleSheet("font-size: 18px;")

    #This function is responsible for the display of error messages in the interface.
    def display_error(self, message):
        self.result_label.setStyleSheet("font-size: 25px;")
        self.result_label.setText(message)


    #This function shows the current weather data in the interface.

    def display_weather(self, data):
        temperature_kel = data["main"]["temp"]

        # Convert Kelvin to Fahrenheit to display
        temperature_fah = (temperature_kel * 9/5) -459.67

        weather_id = data["weather"][0]["id"]

        weather_desc = data["weather"][0]["description"]

        self.result_label.setText(f"{temperature_fah:.0f}°F")
        self.Image_label.setText(self.get_weather_icon(weather_id))
        self.desc_label.setText(weather_desc)
        self.desc_label.setStyleSheet("font-size: 25px;")


    #This function determines the weather emoji based on the weather ID stated in the OpenWeatherMap API.
    @staticmethod
    def get_weather_icon(weather_id):
        if  200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🔥"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " " 
        


    #This function sets the start and end dates for the weather records.
    def val_date(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return start <= end
        except ValueError:
            return False
    
    #This function validates the locartion the user entered.
    def val_location(self, location):
        return bool(location.strip())
    

    #This function is responsible for creating a weather record.
    #It checks if the location and the date range are valid, then creates a record.
    def create_wRecord(self, location, start_date, end_date, weather_data):
        if not self.val_location(location):
            return "Location is invalid."
        if not self.validate_date(start_date, end_date):
            return "Location has an invalid date range."
        
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."
        count = 0
        current_date = start_date
        while current_date <= end_date:

            #Here we check if the record is already in the database.
            self.cursor.execute("INSERT INTO weather_records (location, start_date, end_date, weather_data) VALUES (?, ?, ?, ?)",
                            (location, current_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"), weather_data))
            count += 1
            current_date += timedelta(days=1)

        #commits the date and time of the record, basically the current date and time.
        self.conn.commit()
        
        return f"Weather record created successfully for: {count} days"
    
    #This function allows the user to read the weather record they created
    def read_wRecord(self):
        self.cursor.execute("SELECT location, start_date, end_date, weather_data FROM weather_records")
        rec = self.cursor.fetchall()
        return rec
    
    #This function allows the user to update a weather record
    # by changing the weather data for a specific date, location, and detail such as changing 'rainy' to 'sunny'.
    def update_wRecord(self, location, start_date, end_date, Nweather_data):
        self.cursor.execute(
            "UPDATE weather_records SET weather_data = ? WHERE location = ? AND start_date = ? AND end_date = ?",
            (Nweather_data, location, start_date, end_date)
        )
        self.conn.commit()
    
        if self.cursor.rowcount:
            return "Weather record updated successfully."
        else:
            return "No records found to update or no changes made."
             

    #This function lets the user delete a specific weather record.
    def delete_wRecord(self, location, start_date, end_date):
        self.cursor.execute(
            "DELETE FROM weather_records WHERE location = ? AND start_date = ? AND end_date = ?",
            (location, start_date, end_date)
        )
        self.conn.commit()
        if self.cursor.rowcount:
            return "Weather record deleted successfully."
        else:
            return "No records found to delete."
        

    #This function reads what the user entered for city name or zip code,
    #gathers the start and end dates and weather data,
    #and sends them to the create_WRecord function to store in the SQLite database.
    #Then it confirms by displaying a message in the interface.
    def make_create_record(self):
        location = self.city_input.text().strip() or self.zip_input.text().strip()
        start_date = self.start_date_input.text().strip()
        end_date = self.end_date_input.text().strip()
        weather_data = self.weather_data_input.text().strip()
        result = self.create_wRecord(location, start_date, end_date, weather_data)
        self.result_label.setText(result)

    #This function calls the read_wRecord function which retrieves the records from the weather_records
    #it then converts the records into string format and displays them
    def make_read_record(self):
        records = self.read_wRecord()
        self.result_label.setText(str(records))

    #This function reads the user input for the city name, zip code, start and end date and the Nweather(new weather) data.
    #It then sends them to the update_wRecord function and updates the weather record
    #It also displays a message in the interface
    def make_update_record(self):
        location = self.city_input.text().strip() or self.zip_input.text().strip()
        start_date = self.start_date_input.text().strip()
        end_date = self.end_date_input.text().strip()
        Nweather_data = self.weather_data_input.text().strip()
        result = self.update_wRecord(location, start_date, end_date, Nweather_data)
        self.result_label.setText(result)


    #This function reads what the user entered for city name, zip code, start and end date.
    #It then calls the delete_wRecord function and see if the information matches what's in the records.
    #If it does match, it deletes the record
    #It displays a message wherether the record was deleted or not.
    def make_delete_record(self):
        location = self.city_input.text().strip() or self.zip_input.text().strip()
        start_date = self.start_date_input.text().strip()
        end_date = self.end_date_input.text().strip()
        result = self.delete_wRecord(location, start_date, end_date)
        self.result_label.setText(result)

    #This function displays the Company information in a message box when the 'Info' button is clicked.
    def show_info(self):
        info_text = (
            
            "PM Accelerator is a US based company with a global reach premiering in AI learning and as a development hub,\n"\
            "featuring award-winning AI products and mentors from top-tier companies such as Google, Meta, Apple, and Nvidia.\n"\
            "We offer a dynamic AI PM Bootcamp, designed to empower the next generation of AI professionals through hands-on experience, mentorship, and real-world projects.\n"
        )
        QMessageBox.information(self, "About PM Accelarator", info_text)

   


#Thi code block is the main 'entry point' of the app
#It manages the main interface and starts the application.
##It creates an instance of the WeatherApp class
#It checks for user input to see typing and clicking events.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


