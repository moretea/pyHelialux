"""Pyton library to control (and get information from) Juwel's Helialux Smart Controller."""

import requests
import logging
import re

_LOGGER = logging.getLogger(__name__)

STATUS_VARS_REGEX = re.compile(
    r"(?P<name>[a-zA-Z0-9]+)=((?P<number>\d+)|'(?P<string>[^']+)'|\[(?P<digit_list>(\d+,?)+)\]|\[(?P<string_list>(\"([^\"]+)\",?)+)\]);"
)


def parse_status_vars(status_vars):
    """Extract the variables and their values from a minimal javascript file."""
    output = {}
    for match in STATUS_VARS_REGEX.finditer(status_vars):
        if match["number"] is not None:
            value = int(match["number"])
        elif match["string"] is not None:
            value = match["string"]
        elif match["digit_list"] is not None:
            value = [int(x) for x in match["digit_list"].split(",")]
        elif match["string_list"] is not None:
            value = [
                x[1:-1] for x in match["string_list"].split(",")
            ]  # strip the quotes
        else:
            assert False

        output[match["name"]] = value
    return output


def normalize_brightness(val):
    if val < 0:
        return 0
    elif val > 100:
        return 100
    else:
        return val


def nr_mins_to_formatted(duration):
    """Take a duration in minutes, and return an HH:MM formatted string."""
    hours = int(duration / 60)
    minutes = duration % 60
    return "%02d:%02d" % (hours, minutes)


class Controller:
    """Base Representation of a HeliaLux SmartController"""

    def __init__(self, url):
        self._url = url

    def _statusvars(self):
        _LOGGER.debug("Fetching state from controller")
        response = requests.get(self._url + "/statusvars.js")
        return parse_status_vars(response.content.decode("utf-8"))

    def get_status(self):
        """Fetch the current status from the controller."""
        statusvars = self._statusvars()
        return {
            "currentProfile": statusvars["profile"],
            "currentWhite": statusvars["brightness"][0],
            "currentBlue": statusvars["brightness"][1],
            "currentGreen": statusvars["brightness"][2],
            "currentRed": statusvars["brightness"][3],
            "manualColorSimulationEnabled": statusvars["csimact"] == 1,
            "manualDaytimeSimulationEnabled": statusvars["tsimact"] == 1,
            "deviceTime": nr_mins_to_formatted(statusvars["tsimtime"]),
        }

    def start_manual_color_simulation(self, duration=60):
        requests.post(
            self._url + "/stat",
            {"action": 14, "cswi": "true", "ctime": nr_mins_to_formatted(duration)},
        )

    def set_manual_color(self, white, blue, green, red):
        params = {"action": 10}
        if white is not None:
            params["ch1"] = normalize_brightness(white)
        if blue is not None:
            params["ch2"] = normalize_brightness(blue)
        if green is not None:
            params["ch3"] = normalize_brightness(green)
        if red is not None:
            params["ch4"] = normalize_brightness(red)
        requests.post(self._url + "/stat", params)

    def stop_manual_color_simulation(self):
        requests.post(self._url + "/stat", {"action": 14, "cswi": "false"})
        requests.post(self._url + "/stat", {"action": 10})
