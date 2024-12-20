import mapineqpy as mi

df = mi.data(
    x_source="TGS00010",
    y_source="DEMO_R_MLIFEXP",
    year=2020,
    level="2",
    x_filters={"isced11": "TOTAL", "unit": "PC", "age": "Y_GE15", "freq": "A"},
    y_filters={"unit": "YR", "age": "Y_LT1", "freq": "A"},
)
print(df)


client = mi.MapineqClient()



levels = client.get_levels()
print(levels)  # Should return a list like ["0", "1", "2", "3"]

sources = mi.get_sources(client, level="2", limit=5)
print(sources)  # Should print a list of sources for NUTS level 2

coverage = mi.source_coverage(client, source_name="BD_HGNACE2_R3", limit=1000)
print(coverage)

filters = mi.fetch_filter_options(
    client, 
    source_name="DEMO_R_FIND2", 
    year=2020, 
    level="2"
)
print(filters)  # Should return possible filter values

univariate_data = mi.fetch_univariate_data(
    client, 
    x_source="TGS00010", 
    year=2020, 
    level="2", 
    x_filters={"isced11": "TOTAL", "unit": "PC"}
)
print(univariate_data)  # Should print univariate data points


bivariate_data = mi.fetch_bivariate_data(
    client, 
    x_source="TGS00010", 
    y_source="DEMO_R_MLIFEXP", 
    year=2020, 
    level="2", 
    x_filters={"isced11": "TOTAL", "unit": "PC"}, 
    y_filters={"unit": "YR"}
)
print(bivariate_data)  # Should print bivariate data points
