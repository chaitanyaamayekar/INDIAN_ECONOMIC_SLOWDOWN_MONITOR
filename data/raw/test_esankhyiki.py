# import esankhyiki

# print(dir(esankhyiki))

# print(esankhyiki.list_datasets())

# print(esankhyiki.get_required_metadata_params("PLFS"))

# print(esankhyiki.get_swagger_param_definitions("PLFS"))

# print(esankhyiki.get_required_metadata_params("RBI"))
# print()
# print(esankhyiki.get_swagger_param_definitions("RBI"))
# print(esankhyiki.get_indicators("RBI"))
# indicators = esankhyiki.get_indicators("RBI")
# print(indicators)
# meta = esankhyiki.get_metadata(
#     "RBI",
#     sub_indicator_code=47
# )

# print(meta)
# print(esankhyiki.get_categories())

# meta = esankhyiki.get_metadata("CPI", base_year="2012", level="Group", series="Current")
# print(meta)
# meta_new = esankhyiki.get_metadata("CPI", base_year="2024", level="Group", series="Current")
# print(meta_new)
import esankhyiki

result = esankhyiki.get_data("CPI", {
    "base_year": "2012",
    "year": "2020",
    "series": "Current",
    "state_code": 99,
    "sector_code": 3,
    "group_code": "0",
}, format="dict")

print(result)