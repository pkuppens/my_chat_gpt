"""
Test script for demonstrating code review process.

This module contains intentionally flawed code to demonstrate
the automated code review process. It is not meant to be run.
"""


def convert_to_farhenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Note: This function contains intentional errors for testing purposes.

    Args:
    ----
        celsius (float): Temperature in Celsius.

    Returns:
    -------
        float: Temperature in Fahrenheit (incorrectly calculated).

    """
    # typo in Fahrenheit is intentional, calculation is also wrong, should be celsius * 9/5 + 32
    return celsius * 5 / 9 + 32


def get_weather_report_at_coordinates(coordinates, date_time):
    """
    Get weather report for specific coordinates and time.

    Args:
    ----
        coordinates (list): List of [latitude, longitude].
        date_time (datetime): Date and time for the weather report.

    Returns:
    -------
        list: Weather data [temperature in °C, rain risk (0-1), wave height in m].

    """
    # Dummy function, returns a list of [temperature in °C, risk of rain on a scale 0-1, wave height in m]
    return [28.0, 0.35, 0.85]


def convert_location_to_coordinates(location):
    """
    Convert location name to geographic coordinates.

    Args:
    ----
        location (str): Name of the location.

    Returns:
    -------
        list: Coordinates as [latitude, longitude].

    """
    # Returns dummy coordinates
    return [3.3, -42.0]
