# import esankhyiki
# import yfinance as yf
# import pandas as pd

# YEARS_FY = [f"{y}-{str(y+1)[-2:]}" for y in range(2008, 2025)]  # e.g. "2008-09" ... "2024-25"
# YEARS_CY = [str(y) for y in range(2008, 2027)]  # e.g. "2008" ... "2026"

# # --- CPI: loop over calendar years ---
# cpi_frames = []
# for yr in YEARS_CY:
#     try:
#         df = esankhyiki.get_data("CPI", {
#             "base_year": "2024",
#             "year": yr,
#             "series": "Current",
#         }, format="df")
#         cpi_frames.append(df)
#     except Exception as e:
#         print(f"CPI {yr} skipped: {e}")
# cpi_all = pd.concat(cpi_frames, ignore_index=True)
# cpi_all.to_csv("data/raw/cpi_raw.csv", index=False)

# # --- GDP: loop over financial years ---
# gdp_frames = []
# for fy in YEARS_FY:
#     try:
#         df = esankhyiki.get_data("NAS", {
#             "indicator_code": 1,
#             "base_year": "2022-23",
#             "series": "Current",
#             "frequency_code": 1,
#             "year": fy,          # <-- add this, was missing
#         }, format="df")
#         gdp_frames.append(df)
#     except Exception as e:
#         print(f"GDP {fy} skipped: {e}")
# gdp_all = pd.concat(gdp_frames, ignore_index=True)
# gdp_all.to_csv("data/raw/gdp_raw.csv", index=False)

# # --- IIP: loop over financial years ---
# iip_frames = []
# for fy in YEARS_FY:
#     try:
#         df = esankhyiki.get_data("IIP", {
#             "base_year": "2011-12",
#             "financial_year": fy,
#         }, format="df")
#         iip_frames.append(df)
#     except Exception as e:
#         print(f"IIP {fy} skipped: {e}")
# iip_all = pd.concat(iip_frames, ignore_index=True)
# iip_all.to_csv("data/raw/iip_raw.csv", index=False)

# # --- PLFS: loop over financial years (PLFS only exists from ~2017-18 onward) ---
# plfs_frames = []
# for fy in [f"{y}-{str(y+1)[-2:]}" for y in range(2017, 2025)]:
#     try:
#         df = esankhyiki.get_data("PLFS", {
#             "indicator_code": 3,
#             "frequency_code": 1,
#             "year_type_code": 1,
#             "year": fy,
#             "state_code": 99,
#             "gender_code": 3,
#             "age_code": 1,
#             "sector_code": 3,
#         }, format="df")
#         plfs_frames.append(df)
#     except Exception as e:
#         print(f"PLFS {fy} skipped: {e}")
# plfs_all = pd.concat(plfs_frames, ignore_index=True)
# plfs_all.to_csv("data/raw/plfs_raw.csv", index=False)

# # --- RBI Forex Reserves: check if this single call already returns full history ---
# rbi_df = esankhyiki.get_data("RBI", {
#     "sub_indicator_code": 47,
#     "foreign_exchange_reserve_type_code": 5,
#     "foreign_exchange_reserve_currency_code": 2,
#     "limit": 500
# }, format="df")
# rbi_df.to_csv("data/raw/forex_reserves_raw.csv", index=False)
# print(f"Forex reserves: {len(rbi_df)} rows, date range {rbi_df.iloc[:,0].min()} to {rbi_df.iloc[:,0].max()}")
# # If this doesn't cover 2008-2026, you'll need to paginate similarly using a "page" param if supported

# # --- USD-INR: already full history in one call ---
# inr_df = yf.download("INR=X", start="2008-01-01")
# inr_df.to_csv("data/raw/usdinr_raw.csv")

# print("All historical data fetched and saved.")
import esankhyiki
import yfinance as yf
import pandas as pd
import wbgapi as wb

YEARS_FY = [f"{y}-{str(y+1)[-2:]}" for y in range(2008, 2025)]
YEARS_CY = [str(y) for y in range(2008, 2027)]

# ============================================================
# STEP 1: CPI — pull BOTH series (old 2012 base + new 2024 base)
# ============================================================
# CPI OLD SERIES — with correct filters
cpi_old_frames = []
for yr in range(2011, 2025):
    try:
        df = esankhyiki.get_data("CPI", {
            "base_year": "2012",
            "year": str(yr),
            "series": "Current",
            "state_code": 99,
            "sector_code": 3,
            "group_code": "0",
        }, format="df")
        cpi_old_frames.append(df)
        print(f"CPI old {yr}: {len(df)} rows fetched")
    except Exception as e:
        print(f"CPI old {yr} skipped: {e}")

cpi_old_all = pd.concat(cpi_old_frames, ignore_index=True) if cpi_old_frames else pd.DataFrame()
cpi_old_all.to_csv("data/raw/cpi_old_series_raw.csv", index=False)
print(f"\nTOTAL CPI old: {len(cpi_old_all)} rows")
print(cpi_old_all.head())

# CPI NEW SERIES — with correct filters
cpi_new_frames = []
for yr in ["2025", "2026"]:
    try:
        df = esankhyiki.get_data("CPI", {
            "base_year": "2024",
            "year": yr,
            "series": "Current",
            "state_code": 1,       # All India (NEW series code — different!)
            "sector_code": 3,      # Combined
            "division_code": 0,    # CPI (General)
        }, format="df")
        cpi_new_frames.append(df)
    except Exception as e:
        print(f"CPI new {yr} skipped: {e}")
cpi_new_all = pd.concat(cpi_new_frames, ignore_index=True) if cpi_new_frames else pd.DataFrame()
cpi_new_all.to_csv("data/raw/cpi_new_series_raw.csv", index=False)
print(f"CPI new: {len(cpi_new_all)} rows")

# ============================================================
# STEP 2: GDP Growth (World Bank)
# ============================================================
try:
    gdp_growth = wb.data.DataFrame(
        "NY.GDP.MKTP.KD.ZG",
        economy="IND",
        time=range(2008, 2026)
    )
    gdp_growth = gdp_growth.T
    gdp_growth.index.name = "Year"
    gdp_growth.columns = ["GDP_Growth_%"]
    gdp_growth.to_csv("data/raw/gdp_worldbank_raw.csv")
    print(f"GDP Growth: {len(gdp_growth)} rows")
except Exception as e:
    print(f"GDP Growth download failed: {e}")

# ============================================================
# STEP 3: IIP — filtering happens later in cleaning
# ============================================================
iip_frames = []
for yr in range(2012, 2027):
    for month_code in range(1, 13):
        try:
            df = esankhyiki.get_data("IIP", {
                "base_year": "2011-12",
                "year": yr,
                "month_code": month_code,
                "category_code": 4,   # General
            }, format="df")
            iip_frames.append(df)
        except Exception as e:
            print(f"IIP {yr}-{month_code} skipped: {e}")

iip_all = pd.concat(iip_frames, ignore_index=True) if iip_frames else pd.DataFrame()
iip_all.to_csv("data/raw/iip_raw.csv", index=False)
print(f"IIP monthly: {len(iip_all)} rows")
print("Unique years:", sorted(iip_all['year'].unique()) if len(iip_all) else "none")
print(iip_all.head())

# ============================================================
# STEP 4: PLFS — filtering happens later in cleaning
# ============================================================
plfs_frames = []
for fy in [f"{y}-{str(y+1)[-2:]}" for y in range(2017, 2025)]:
    try:
        df = esankhyiki.get_data("PLFS", {
            "indicator_code": 3,
            "frequency_code": 1,
            "year_type_code": 1,
            "year": fy,
            "state_code": 99,
            "gender_code": 3,
            "age_code": 1,
            "sector_code": 3,
        }, format="df")
        plfs_frames.append(df)
    except Exception as e:
        print(f"PLFS {fy} skipped: {e}")

plfs_all = pd.concat(plfs_frames, ignore_index=True) if plfs_frames else pd.DataFrame()
plfs_all.to_csv("data/raw/plfs_raw.csv", index=False)

print(f"PLFS: {len(plfs_all)} rows")

# ============================================================
# STEP 5: Forex reserves
# ============================================================
forex_frames = []
for yr in range(2001, 2027):
    try:
        df = esankhyiki.get_data("RBI", {
            "sub_indicator_code": 47,
            "foreign_exchange_reserve_type_code": 5,
            "foreign_exchange_reserve_currency_code": 2,
            "year": yr,
        }, format="df")
        forex_frames.append(df)
    except Exception as e:
        print(f"Forex {yr} skipped: {e}")

forex_all = pd.concat(forex_frames, ignore_index=True) if forex_frames else pd.DataFrame()
forex_all.to_csv("data/raw/forex_reserves_raw.csv", index=False)
print(f"Forex: {len(forex_all)} rows, years: {sorted(forex_all['year'].unique())}")

# ============================================================
# STEP 6: USD-INR
# ============================================================
try:
    inr_df = yf.download("INR=X", start="2008-01-01", auto_adjust=True)

    if isinstance(inr_df.columns, pd.MultiIndex):
        inr_df.columns = inr_df.columns.get_level_values(0)

    inr_df = inr_df.reset_index()

    inr_df.to_csv("data/raw/usdinr_raw.csv", index=False)

    print(f"USD-INR: {len(inr_df)} rows")
    print(inr_df.head(3))

except Exception as e:
    print(f"USD-INR download failed: {e}")

print("\nDone. Check the row counts above for each dataset.")