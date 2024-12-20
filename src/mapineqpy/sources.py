import requests
import pandas as pd
from mapineqpy.config import BASE_API_ENDPOINT, USER_AGENT


def sources(level, year=None, limit=1000):
    """
    Get a list of available data sources.

    Args:
        level (str): A string specifying the NUTS level ("0", "1", "2", "3").
        year (int, optional): An integer specifying the year. Default is None.
        limit (int): Maximum number of results to fetch. Default is 1000.

    Returns:
        pd.DataFrame: A DataFrame with source metadata, containing:
            - source_name: Name of the data source
            - short_description: Short description of the data source
            - description: Full description of the data source

    Example:
        >>> mi_sources("3", limit=10)
        >>> mi_sources("3", year=2020)
    """
    if level not in ["0", "1", "2", "3"]:
        raise ValueError(f"Invalid level: {level}. Must be one of '0', '1', '2', '3'.")
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("`limit` must be a positive integer.")

    endpoint = (
        f"{BASE_API_ENDPOINT}get_source_by_nuts_level/items.json"
        if year is None
        else f"{BASE_API_ENDPOINT}get_source_by_year_nuts_level/items.json"
    )
    query_params = {"_level": level, "limit": limit}
    if year is not None:
        query_params["_year"] = year

    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        params=query_params,
    )
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)
    df.rename(
        columns={
            "f_resource": "source_name",
            "f_short_description": "short_description",
            "f_description": "description",
        },
        inplace=True,
    )
    return df[["source_name", "short_description", "description"]]

def source_coverage(source_name, limit=1500):
    """
    Get the NUTS level and Year coverage for a specific data source.

    Args:
        source_name (str): The name of the data source.
        limit (int): Maximum number of results to fetch. Default is 1500.

    Returns:
        pd.DataFrame: A DataFrame with coverage metadata:
            - nuts_level: NUTS level
            - year: Year
            - source_name: Name of the data source
            - short_description: Short description of the data source
            - description: Full description of the data source

    Example:
        >>> mi_source_coverage("BD_HGNACE2_R3")
    """
    endpoint = f"{BASE_API_ENDPOINT}get_year_nuts_level_from_source/items.json"
    query_params = {"_resource": source_name, "limit": limit}
    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        params=query_params,
    )
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)
    df.rename(
        columns={
            "f_level": "nuts_level",
            "f_year": "year",
        },
        inplace=True,
    )

    df["source_name"] = source_name
    df["short_description"] = "Settlement type"  # Example; adjust dynamically if possible
    df["description"] = "Satellite-based settlement types based on imagery"  # Example

    return df[
        ["nuts_level", "year", "source_name", "short_description", "description"]
    ]
