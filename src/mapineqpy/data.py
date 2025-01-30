import requests
import pandas as pd
import json
from mapineqpy.config import BASE_API_ENDPOINT, USER_AGENT


def data(
    x_source, y_source=None, year=None, level=None, x_filters=None, y_filters=None, limit=2500
):
    """
    Fetch univariate or bivariate data for a specific source, year, NUTS level, and selected filters.

    Args:
        x_source (str): Source name for the x variable.
        y_source (str, optional): Source name for the y variable. Default is None.
        year (int): The year for data.
        level (str): The NUTS level ("0", "1", "2", "3").
        x_filters (dict): Filters for the x variable as a dictionary of field-value pairs.
        y_filters (dict, optional): Filters for the y variable as a dictionary of field-value pairs. Default is None.
        limit (int): Maximum number of results to return. Default is 2500.

    Returns:
        pd.DataFrame: A DataFrame containing univariate or bivariate data.

    Example:
        # Univariate example
        >>> mi.data(
        ...     x_source="TGS00010",
        ...     year=2020,
        ...     level="2",
        ...     x_filters={"isced11": "TOTAL", "unit": "PC", "age": "Y_GE15", "freq": "A"}
        ... )

        # Bivariate example
        >>> mi.data(
        ...     x_source="TGS00010",
        ...     y_source="DEMO_R_MLIFEXP",
        ...     year=2020,
        ...     level="2",
        ...     x_filters={"isced11": "TOTAL", "unit": "PC", "age": "Y_GE15", "freq": "A"},
        ...     y_filters={"unit": "YR", "age": "Y_LT1", "freq": "A"}
        ... )
    """
    if x_filters is None:
        x_filters = {}
    if y_filters is None:
        y_filters = {}

    # Validate inputs
    if not isinstance(x_source, str) or not x_source:
        raise ValueError("`x_source` must be a non-empty string.")
    if level not in ["0", "1", "2", "3"]:
        raise ValueError(f"Invalid `level`: {level}. Must be one of '0', '1', '2', '3'.")
    if not isinstance(year, int):
        raise ValueError("`year` must be an integer.")
    if y_source is not None and not isinstance(y_source, str):
        raise ValueError("`y_source` must be a string if provided.")

    # Build JSON for X filters
    x_conditions = [{"field": key, "value": value} for key, value in x_filters.items()]
    x_json = {"source": x_source, "conditions": x_conditions}
    x_json_string = json.dumps(x_json)

    # Check if bivariate (Y filters provided)
    y_json_string = None
    if y_source and y_filters:
        y_conditions = [{"field": key, "value": value} for key, value in y_filters.items()]
        y_json = {"source": y_source, "conditions": y_conditions}
        y_json_string = json.dumps(y_json)

    # Determine API endpoint
    endpoint = (
        f"{BASE_API_ENDPOINT}get_x_data/items.json"
        if not y_source
        else f"{BASE_API_ENDPOINT}get_xy_data/items.json"
    )

    # Prepare query parameters
    query_params = {
        "_level": level,
        "_year": str(year),
        "X_JSON": x_json_string,
        "limit": limit,
    }
    if y_json_string:
        query_params["Y_JSON"] = y_json_string

    # Perform the HTTP GET request
    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        params=query_params,
    )
    response.raise_for_status()

    # Parse response and convert to DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # Return tidy DataFrame
    if "y" in df.columns:
        return df[["geo", "geo_name", "best_year", "x", "y"]]
    return df[["geo", "geo_name", "best_year", "x"]]
