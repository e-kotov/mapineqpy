# File: mapineqpy/functions.py

import requests
from mapineqpy.config import BASE_API_ENDPOINT, USER_AGENT

def nuts_levels():
    """
    Get a list of available NUTS levels.

    Returns:
        list: A list of valid NUTS levels as strings that will be accepted by other functions.

    Example:
        >>> get_nuts_levels()
        ['3', '2', '1', '0']
    """
    # Construct the full URL
    url_endpoint = f"{BASE_API_ENDPOINT}get_levels/items.json"

    # Perform the HTTP GET request
    response = requests.get(
        url_endpoint,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    # Raise an error for bad responses
    response.raise_for_status()

    # Parse and return the JSON response
    response_data = response.json()
    return [item["f_level"] for item in response_data]
