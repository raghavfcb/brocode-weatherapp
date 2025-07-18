#weather application using PyQt5 and requests 
import sys, requests
from PyQt5.QtWidgets import (QApplication, QWidget, 
                                        QPushButton, QLineEdit, QLabel,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("weather.jpg"))
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 300, 400, 500)
        self.title_label = QLabel("What's the weather today?", self)
        self.enter_city = QLineEdit(self)
        self.weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel( self)
        self.weather_emoji = QLabel( self)
        self.climate_label = QLabel( self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.enter_city)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.weather_emoji)
        vbox.addWidget(self.climate_label)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.weather_emoji.setAlignment(Qt.AlignCenter)
        self.climate_label.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)
        self.title_label.setObjectName("title_label")
        self.temp_label.setObjectName("temp_label")
        self.weather_button.setObjectName("weather_button")
        self.weather_emoji.setObjectName("weather_emoji")
        self.climate_label.setObjectName("climate_label")


        self.setStyleSheet("""

            QLabel#title_label{font-size: 50px; font-weight: bold; font-family: Calibri; background-color: hsl(198, 100%, 97%); border-radius: 12px; } 
                           
            QLabel#temp_label{font-size: 50px; font-weight: bold; font-family: Calibri; background-color: hsl(198, 100%, 97%);   } 
            QPushButton#weather_button{font-size: 45px; font-weight: bold; font-family: calibri; border-radius: 12px; border: 3px solid black}
            QPushButton#weather_button:hover{background-color: hsl(198, 100%, 90%); border: 3px solid black; color: black}
            QLineEdit{font-size: 40px; font-family: Calibri; border-radius: 12px;  border: 3px solid black}
                           
            QLabel#weather_emoji{font-size: 50px; font-weight: bold; font-family: Segoe UI Emoji; background-color: hsl(198, 100%, 97%);  }
            QLabel#climate_label{font-size: 50px; font-weight: bold; font-family: Segoe UI Emoji; background-color: hsl(198, 100%, 97%);  }


""")
        self.weather_button.clicked.connect(self.get_weather)

        
    def get_weather(self):
        api_key = "360b2e99a878f3597faa7742e06e4b8d"
        city = self.enter_city.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['cod'] == 200:
                self.display_weather(data)
            else:
                print(data)
        except requests.exceptions.HTTPError as httperror:
            match response.status_code:
                case 400:
                    self.errors(f"Bad Request\nPlease check the city name and try again.")
                case 401:
                    self.errors("Unauthorized Request\nInvalid API key.")
                case 403:
                    self.errors("Forbidden\nAccess Denied.")
                case 404:
                    self.errors("Not Found\nCity Not Found.")
                case 500:
                    self.errors("Internal Server Error\nPlease try again later.")
                case 502:
                    self.errors("Bad Gateway\nInvalid response from the server..")
                case 503:
                    self.errors("Service Unavailable\nThe server is currently unavailable.")
                case 504:
                   self.errors("Gateway Timeout\nThe server did not receive a timely response from the upstream server.")
                case _:
                    self.errors(f"HTTP Error {httperror} occured, Please try again later.")

        except requests.exceptions.ConnectionError:
            print("Connection Error\nPlease check your internet connection.")
        except requests.exceptions.Timeout:
            print("Timeout Error\nThe request timed out.")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects\nCheck the URL and try again.")        
        except requests.exceptions.RequestException as req_err:
            print(f"Request Error : {req_err}")
            

    def errors(self, message):
        self.temp_label.setText(message)
        self.temp_label.setStyleSheet("FONT-SIZE: 40PX")
        self.weather_emoji.clear()
        self.climate_label.clear()

    def display_weather(self, data):
       temp_k = data["main"]["temp"]
       temp_c = temp_k  - 273.15
       temp_f = (temp_c * 9/5) + 32
       weather_id = data["weather"][0]["id"]
       self.weather_emoji.setText(self.weather_icon(weather_id))
       self.temp_label.setText(f"{temp_c:.0f}°C     or    {temp_f:.0f}°F")
       self.temp_label.setStyleSheet("font-size:75 px;")
       climate = data["weather"][0]["description"].capitalize()
       self.climate_label.setText(f"{climate}")
       self.climate_label.setStyleSheet("font-size:75 px;")

    @staticmethod
    def weather_icon(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        if weather_id == 701:
            return "🌫️"
        elif weather_id == 711:
            return "💨"
        elif weather_id == 721:
            return "🌫️"
        elif weather_id == 731:
            return "💨"
        elif weather_id== 741:
                 return "🌫️"
        elif weather_id== 751:
                return "🌪️"
        elif weather_id == 761:
                return  "🌪️"
        elif weather_id == 762:
            return  "🌪️"
        elif weather_id == 771:
                return  "🌪️"
        elif weather_id == 781:
            return  "🌪️"
        elif weather_id == 800:
            return  "☀️"
        elif 801 <= weather_id <= 804:
            return  "🌤️"
        else:
            return " "
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())