# This is a dummy script to test the review process. It is not meant to be run, only to have it reviewed.


def convert_to_farhenheit(celsius):
    # typo in Fahrenheit is intentional, calculation is also wrong, should be celsius * 9/5 + 32
    return celsius * 5 / 9 + 32


def get_weather_report_at_coordinates(coordinates, date_time):
    # Dummy function, returns a list of [temperature in °C, risk of rain on a scale 0-1, wave height in m]
    return [28.0, 0.35, 0.85]


def convert_location_to_coordinates(location):
    # Returns dummy coordinates
    return [3.3, -42.0]
