import pandas as pd

# files = {
#     "CPI (old, 2012 base)": "data/raw/cpi_old_series_raw.csv",
#     "CPI (new, 2024 base)": "data/raw/cpi_new_series_raw.csv",
#     "GDP (World Bank)": "data/raw/gdp_worldbank_raw.csv",
#     "IIP": "data/raw/iip_raw.csv",
#     "PLFS": "data/raw/plfs_raw.csv",
#     "Forex": "data/raw/forex_reserves_raw.csv",
#     "USD-INR": "data/raw/usdinr_raw.csv",
# }


# for name, path in files.items():
#     print(f"\n{'='*50}\n{name}\n{'='*50}")
#     try:
#         df = pd.read_csv(path)
#         print(f"Shape: {df.shape}")
#         print(f"Columns: {list(df.columns)}")
#         print(df.head(3))
#     except Exception as e:
#         print(f"Error reading {path}: {e}")
import pandas as pd

old = pd.read_csv("data/raw/cpi_old_series_raw.csv")
new = pd.read_csv("data/raw/cpi_new_series_raw.csv")

print("OLD series:")
print(f"Shape: {old.shape}, Years: {sorted(old['year'].unique())}")
print(old.head())

print("\nNEW series:")
print(f"Shape: {new.shape}, Years: {sorted(new['year'].unique())}")
print(new.head())