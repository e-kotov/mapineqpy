import mapineqpy as mi

df = mi.data(
    x_source="TGS00010",
    y_source="DEMO_R_MLIFEXP",
    year=2020,
    level="2",
    x_filters={"isced11": "TOTAL", "unit": "PC", "age": "Y_GE15", "freq": "A", "sex": "T"},
    y_filters={"unit": "YR", "age": "Y_LT1", "freq": "A", "sex": "T"},
)
print(df)


levels = mi.nuts_levels()
print(levels)  # Should return a list like ["0", "1", "2", "3"]

sources = mi.sources(level="2", limit=5)
print(sources)  # Should print a list of sources for NUTS level 2

coverage = mi.source_coverage(source_name="BD_HGNACE2_R3", limit=2500)
print(coverage)

filters = mi.source_filters(
    source_name="DEMO_R_FIND2", 
    year=2020, 
    level="2"
)
print(filters)  # Should return possible filter values
