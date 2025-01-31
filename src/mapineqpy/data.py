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
        pd.DataFrame: A DataFrame containing univariate or bivariate data with the following columns:

        - `geo` (str): (NUTS) region code at the requested level.
        - `geo_name` (str): Name of the (NUTS) region.
        - `geo_source` (str): Source type of the spatial units (e.g., "NUTS").
        - `geo_year` (int): Year of the (NUTS) region classification.
        - `x_year` (int): The year of the predictor variable (X) (renamed from `predictor_year` or `data_year`).
        - `y_year` (int, optional): The year of the outcome variable (Y) (renamed from `outcome_year`).
        - `x` (float): The value of the univariate variable.
        - `y` (float, optional): The value of the y variable (only included when `y_source` is provided).

    Notes:
        - If `y_source` is **not** provided, the returned DataFrame contains only univariate data (`x`).
        - If `y_source` **is** provided, the returned DataFrame includes both predictor (`x`) and outcome (`y`) variables.
        - Some regions may have missing (`NaN`) values for `x` or `y`, indicating unavailable data.

    Example:
        # Univariate example
        >>> import mapineqpy as mi
        >>> mi.data(
        ...     x_source="TGS00010",
        ...     year=2020,
        ...     level="2",
        ...     x_filters={"isced11": "TOTAL", "unit": "PC", "age": "Y_GE15", "freq": "A"}
        ... )

        # Bivariate example
        >>> import mapineqpy as mi
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
    x_json_string = json.dumps(x_json, separators=(",", ":"))  # Compact JSON format

    # Check if bivariate (Y filters provided)
    y_json_string = None
    if y_source and y_filters:
        y_conditions = [{"field": key, "value": value} for key, value in y_filters.items()]
        y_json = {"source": y_source, "conditions": y_conditions}
        y_json_string = json.dumps(y_json, separators=(",", ":"))

    # Determine API endpoint
    endpoint = (
        f"{BASE_API_ENDPOINT}get_x_data/items.json"
        if not y_source
        else f"{BASE_API_ENDPOINT}get_xy_data/items.json"
    )

    # Prepare query parameters
    query_params = {
        "_level": level,
        "limit": limit,
        "X_JSON": x_json_string,
    }

    if y_source:
        query_params["_predictor_year"] = str(year)
        query_params["_outcome_year"] = str(year)
    else:
        query_params["_year"] = str(year)

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
    df = pd.DataFrame(response.json())

    # Define expected columns based on whether y_source is specified
    if y_source:
        expected_columns = ["geo", "geo_name", "geo_source", "geo_year", "predictor_year", "outcome_year", "x", "y"]
    else:
        expected_columns = ["geo", "geo_name", "geo_source", "geo_year", "data_year", "x"]

    # Check for missing expected columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"The following expected columns are missing from the response: {', '.join(missing_columns)}. "
            "The API may be down or might have changed. Please try again later. If the error persists, "
            "please open an issue on GitHub at <https://github.com/e-kotov/mapineqr/issues>."
        )

    # Rename columns to match documentation
    rename_mapping = {
        "predictor_year": "x_year",
        "outcome_year": "y_year",
        "data_year": "x_year"
    }
    df.rename(columns={k: v for k, v in rename_mapping.items() if k in df.columns}, inplace=True)

    # Select and reorder columns
    final_columns = ["geo", "geo_name", "geo_source", "geo_year", "x_year", "y_year", "x", "y"]
    df = df[[col for col in final_columns if col in df.columns]]

    return df
