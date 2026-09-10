import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        self.unit = "C"
        self.weather_data = None

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="WEATHER FORECAST DASHBOARD",
            font=("Segoe UI", 24, "bold"),
            bg="#101820",
            fg="#00D4FF"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Real-time weather information and forecast",
            font=("Segoe UI", 10),
            bg="#101820",
            fg="#AAB8C2"
        ).pack()

        search = tk.Frame(
            self.root,
            bg="#182530",
            padx=15,
            pady=15
        )
        search.pack(fill="x", padx=30, pady=15)

        self.city = tk.Entry(
            search,
            font=("Segoe UI", 12),
            width=28,
            bg="#0B1116",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.city.pack(side="left", padx=8, ipady=7)

        tk.Button(
            search,
            text="GET WEATHER",
            command=self.get_weather,
            bg="#00A8CC",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            search,
            text="MY LOCATION",
            command=self.detect_location,
            bg="#334653",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        self.unit_button = tk.Button(
            search,
            text="°C",
            command=self.change_unit,
            bg="#00A8CC",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=5
        )
        self.unit_button.pack(side="left", padx=5)

        self.status = tk.Label(
            self.root,
            text="Enter a city name to continue.",
            bg="#101820",
            fg="#8FA4B2",
            font=("Segoe UI", 9)
        )
        self.status.pack()

        current = tk.Frame(
            self.root,
            bg="#182530",
            padx=25,
            pady=20
        )
        current.pack(fill="x", padx=30, pady=10)

        tk.Label(
            current,
            text="CURRENT WEATHER",
            font=("Segoe UI", 13, "bold"),
            bg="#182530",
            fg="#00D4FF"
        ).pack(anchor="w")

        body = tk.Frame(current, bg="#182530")
        body.pack(fill="x", pady=10)

        self.icon = tk.Label(
            body,
            text="🌤️",
            font=("Segoe UI", 55),
            bg="#182530",
            fg="white"
        )
        self.icon.pack(side="left", padx=25)

        info = tk.Frame(body, bg="#182530")
        info.pack(side="left")

        self.location = tk.Label(
            info,
            text="No location",
            font=("Segoe UI", 18, "bold"),
            bg="#182530",
            fg="white"
        )
        self.location.pack(anchor="w")

        self.temperature = tk.Label(
            info,
            text="--°C",
            font=("Segoe UI", 38, "bold"),
            bg="#182530",
            fg="#00D4FF"
        )
        self.temperature.pack(anchor="w")

        self.condition = tk.Label(
            info,
            text="Weather condition",
            font=("Segoe UI", 11),
            bg="#182530",
            fg="#B8C4CE"
        )
        self.condition.pack(anchor="w")

        details = tk.Frame(body, bg="#182530")
        details.pack(side="right", padx=60)

        self.humidity = self.detail_label(
            details,
            "Humidity: --"
        )

        self.wind = self.detail_label(
            details,
            "Wind Speed: --"
        )

        self.feels = self.detail_label(
            details,
            "Feels Like: --"
        )

        self.pressure = self.detail_label(
            details,
            "Pressure: --"
        )

        tabs = ttk.Notebook(self.root)
        tabs.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.hourly = tk.Frame(
            tabs,
            bg="#182530"
        )

        self.daily = tk.Frame(
            tabs,
            bg="#182530"
        )

        tabs.add(
            self.hourly,
            text="NEXT 6 HOURS"
        )

        tabs.add(
            self.daily,
            text="5-DAY FORECAST"
        )

        self.show_message(
            self.hourly,
            "Search for a city to view hourly forecast."
        )

        self.show_message(
            self.daily,
            "Search for a city to view 5-day forecast."
        )

    def detail_label(self, parent, text):
        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10),
            bg="#182530",
            fg="white"
        )
        label.pack(
            anchor="w",
            pady=4
        )
        return label

    def show_message(self, parent, text):
        tk.Label(
            parent,
            text=text,
            bg="#182530",
            fg="#8FA4B2",
            font=("Segoe UI", 10)
        ).pack(pady=50)

    def get_weather(self):
        city = self.city.get().strip()

        if not city:
            self.error(
                "Please enter a city name."
            )
            return

        self.status.config(
            text="Loading weather information...",
            fg="#8FA4B2"
        )

        self.root.update()

        try:
            geo_url = (
                "https://geocoding-api.open-meteo.com/"
                "v1/search"
            )

            geo_params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            geo_response = requests.get(
                geo_url,
                params=geo_params,
                timeout=10
            )

            geo_response.raise_for_status()

            geo_data = geo_response.json()

            if "results" not in geo_data:
                self.error("City not found.")
                return

            location = geo_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]

            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
            )

            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "weather_code,"
                    "wind_speed_10m,"
                    "surface_pressure"
                ),
                "hourly": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min"
                ),
                "forecast_days": 5,
                "timezone": "auto"
            }

            weather_response = requests.get(
                weather_url,
                params=weather_params,
                timeout=10
            )

            weather_response.raise_for_status()

            self.weather_data = weather_response.json()

            self.location_name = location["name"]
            self.country = location.get(
                "country",
                ""
            )

            self.show_current()
            self.show_hourly()
            self.show_daily()

            self.status.config(
                text="Weather updated successfully.",
                fg="#55D68A"
            )

        except requests.exceptions.Timeout:
            self.error(
                "Request timed out."
            )

        except requests.exceptions.ConnectionError:
            self.error(
                "Check your internet connection."
            )

        except requests.exceptions.RequestException:
            self.error(
                "Unable to retrieve weather data."
            )

        except Exception as error:
            self.error(str(error))

    def show_current(self):
        current = self.weather_data["current"]

        temperature = current[
            "temperature_2m"
        ]

        apparent = current[
            "apparent_temperature"
        ]

        humidity = current[
            "relative_humidity_2m"
        ]

        wind = current[
            "wind_speed_10m"
        ]

        pressure = current[
            "surface_pressure"
        ]

        code = current[
            "weather_code"
        ]

        self.location.config(
            text=f"{self.location_name}, {self.country}"
        )

        self.temperature.config(
            text=self.temp_text(
                temperature
            )
        )

        self.condition.config(
            text=self.weather_description(code)
        )

        self.humidity.config(
            text=f"Humidity: {humidity}%"
        )

        self.wind.config(
            text=f"Wind Speed: {wind:.1f} km/h"
        )

        self.feels.config(
            text=f"Feels Like: {self.temp_text(apparent)}"
        )

        self.pressure.config(
            text=f"Pressure: {pressure:.0f} hPa"
        )

        self.icon.config(
            text=self.weather_icon(code)
        )

    def show_hourly(self):
        for widget in self.hourly.winfo_children():
            widget.destroy()

        hourly = self.weather_data["hourly"]

        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        codes = hourly["weather_code"]

        current_time = datetime.now()

        start_index = 0

        for i, value in enumerate(times):
            try:
                weather_time = datetime.fromisoformat(
                    value
                )

                if weather_time >= current_time:
                    start_index = i
                    break

            except Exception:
                pass

        for i in range(
            start_index,
            min(start_index + 6, len(times))
        ):
            card = tk.Frame(
                self.hourly,
                bg="#223541",
                width=145,
                height=190
            )

            card.pack(
                side="left",
                padx=7,
                pady=20
            )

            card.pack_propagate(False)

            time_text = datetime.fromisoformat(
                times[i]
            ).strftime("%I:%M %p")

            tk.Label(
                card,
                text=time_text,
                bg="#223541",
                fg="#00D4FF",
                font=("Segoe UI", 10, "bold")
            ).pack(pady=8)

            tk.Label(
                card,
                text=self.weather_icon(
                    codes[i]
                ),
                bg="#223541",
                fg="white",
                font=("Segoe UI", 28)
            ).pack()

            tk.Label(
                card,
                text=self.temp_text(
                    temperatures[i]
                ),
                bg="#223541",
                fg="white",
                font=("Segoe UI", 13, "bold")
            ).pack(pady=5)

            tk.Label(
                card,
                text=self.weather_description(
                    codes[i]
                ),
                bg="#223541",
                fg="#B8C4CE",
                font=("Segoe UI", 8),
                wraplength=120
            ).pack()

    def show_daily(self):
        for widget in self.daily.winfo_children():
            widget.destroy()

        daily = self.weather_data["daily"]

        dates = daily["time"]
        maximum = daily["temperature_2m_max"]
        minimum = daily["temperature_2m_min"]
        codes = daily["weather_code"]

        for i in range(
            min(5, len(dates))
        ):
            card = tk.Frame(
                self.daily,
                bg="#223541",
                width=160,
                height=190
            )

            card.pack(
                side="left",
                padx=7,
                pady=20
            )

            card.pack_propagate(False)

            day = datetime.strptime(
                dates[i],
                "%Y-%m-%d"
            ).strftime("%a, %d %b")

            tk.Label(
                card,
                text=day,
                bg="#223541",
                fg="#00D4FF",
                font=("Segoe UI", 10, "bold")
            ).pack(pady=8)

            tk.Label(
                card,
                text=self.weather_icon(
                    codes[i]
                ),
                bg="#223541",
                font=("Segoe UI", 28)
            ).pack()

            tk.Label(
                card,
                text=f"High: {self.temp_text(maximum[i])}",
                bg="#223541",
                fg="white",
                font=("Segoe UI", 9, "bold")
            ).pack(pady=3)

            tk.Label(
                card,
                text=f"Low: {self.temp_text(minimum[i])}",
                bg="#223541",
                fg="white",
                font=("Segoe UI", 9)
            ).pack()

            tk.Label(
                card,
                text=self.weather_description(
                    codes[i]
                ),
                bg="#223541",
                fg="#B8C4CE",
                font=("Segoe UI", 8),
                wraplength=130
            ).pack(pady=5)

    def detect_location(self):
        try:
            response = requests.get(
                "https://ipinfo.io/json",
                timeout=10
            )

            data = response.json()

            city = data.get("city")

            if not city:
                self.error(
                    "Location could not be detected."
                )
                return

            self.city.delete(
                0,
                tk.END
            )

            self.city.insert(
                0,
                city
            )

            self.get_weather()

        except Exception:
            self.error(
                "Unable to detect your location."
            )

    def change_unit(self):
        if self.unit == "C":
            self.unit = "F"
            self.unit_button.config(
                text="°F"
            )
        else:
            self.unit = "C"
            self.unit_button.config(
                text="°C"
            )

        if self.weather_data:
            self.show_current()
            self.show_hourly()
            self.show_daily()

    def temp_text(self, value):
        if self.unit == "C":
            return f"{value:.1f}°C"

        fahrenheit = (
            value * 9 / 5
        ) + 32

        return f"{fahrenheit:.1f}°F"

    def weather_description(self, code):
        descriptions = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Rime Fog",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Snow",
            75: "Heavy Snow",
            80: "Rain Showers",
            81: "Rain Showers",
            82: "Heavy Showers",
            95: "Thunderstorm",
            96: "Thunderstorm",
            99: "Thunderstorm"
        }

        return descriptions.get(
            code,
            "Unknown Weather"
        )

    def weather_icon(self, code):
        if code == 0:
            return "☀️"

        if code in [1, 2]:
            return "🌤️"

        if code == 3:
            return "☁️"

        if code in [45, 48]:
            return "🌫️"

        if code in [51, 53, 55]:
            return "🌦️"

        if code in [61, 63, 65, 80, 81, 82]:
            return "🌧️"

        if code in [71, 73, 75]:
            return "❄️"

        if code in [95, 96, 99]:
            return "⛈️"

        return "🌤️"

    def error(self, message):
        self.status.config(
            text=f"Error: {message}",
            fg="#FF6B6B"
        )


def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()