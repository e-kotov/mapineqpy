import requests
import pandas as pd
import json
from mapineqpy.config import BASE_API_ENDPOINT, USER_AGENT


def source_filters(source_name, year, level, filters=None, limit=40):
    """
    Fetch possible filtering values for a given source, year, and NUTS level.

    Args:
        source_name (str): The name of the data source (f_resource).
        year (int): The year for filtering.
        level (str): The NUTS level ("0", "1", "2", "3").
        filters (dict, optional): A dictionary where the keys are filter fields and
                                  values are the selected filter values. Default is None.
        limit (int): Maximum number of results to fetch. Default is 40.

    Returns:
        pd.DataFrame: A DataFrame with fields, labels, and their possible values for filtering:
            - field: Filter field name.
            - field_label: Filter field label.
            - label: Value label.
            - value: Value.
    """
    if filters is None:
        filters = {}

    # Validate inputs
    if not isinstance(source_name, str) or not source_name:
        raise ValueError("`source_name` must be a non-empty string.")
    if level not in ["0", "1", "2", "3"]:
        raise ValueError(f"Invalid `level`: {level}. Must be one of '0', '1', '2', '3'.")
    if not isinstance(year, int):
        raise ValueError("`year` must be an integer.")

    # Convert filters to the required structure
    selected = [{"field": key, "value": value} for key, value in filters.items()]

    # Prepare JSON for source selections
    source_selections = {
        "year": str(year),
        "level": level,
        "selected": selected,
    }
    source_selections_json = json.dumps(source_selections)

    # Prepare API endpoint and parameters
    endpoint = f"{BASE_API_ENDPOINT}get_column_values_source_json/items.json"
    query_params = {
        "_resource": source_name,
        "source_selections": source_selections_json,
        "limit": limit,
    }

    # Perform the HTTP GET request
    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        params=query_params,
    )
    response.raise_for_status()

    # Parse the JSON response
    try:
        data = response.json()  # Ensure this handles both list and dict cases
    except ValueError as e:
        raise ValueError(f"Failed to parse JSON response: {e}")

    # If the response is already a list, iterate over it directly
    if isinstance(data, list):
        records = []
        for item in data:
            field = item.get("field")
            field_label = item.get("field_label")
            for field_value in item.get("field_values", []):
                records.append({
                    "field": field,
                    "field_label": field_label,
                    "label": field_value.get("label"),
                    "value": field_value.get("value"),
                })
        return pd.DataFrame(records)

    raise ValueError("Unexpected response format from the API.")
