import pandas as pd
import numpy as np

merged = pd.read_csv("data/clean/merged_indicators.csv", parse_dates=['date'])
merged = merged.set_index('date').sort_index()

# --- Rolling z-scores (3-year trailing window = 36 months) ---
WINDOW = 36

def rolling_zscore(series, window=WINDOW):
    roll_mean = series.rolling(window, min_periods=12).mean()
    roll_std = series.rolling(window, min_periods=12).std()
    return (series - roll_mean) / roll_std

merged['z_cpi_inflation'] = rolling_zscore(merged['cpi_yoy_inflation'])
merged['z_iip_growth'] = rolling_zscore(merged['iip_growth_rate'])
merged['z_forex'] = rolling_zscore(merged['forex_reserves_usd_mn'])
merged['z_usdinr'] = rolling_zscore(merged['usdinr_rate'])

# --- Flip signs so all point the same "bad" direction ---
merged['risk_cpi'] = merged['z_cpi_inflation']       # high inflation = bad, keep as-is
merged['risk_iip'] = -merged['z_iip_growth']          # high growth = good, flip
merged['risk_forex'] = -merged['z_forex']             # high reserves = good, flip
merged['risk_usdinr'] = merged['z_usdinr']            # rupee weakening = bad, keep as-is

# --- Composite index: average of available risk components ---
risk_cols = ['risk_cpi', 'risk_iip', 'risk_forex', 'risk_usdinr']
merged['slowdown_risk_index'] = merged[risk_cols].mean(axis=1, skipna=True)
merged['components_available'] = merged[risk_cols].notna().sum(axis=1)

merged = merged.reset_index()
merged.to_csv("data/clean/slowdown_risk_index.csv", index=False)

print(f"Index built: {len(merged)} rows")
print("\nLast 15 rows:")
print(merged[['date', 'slowdown_risk_index', 'components_available']].tail(15))

print("\nComponents available breakdown:")
print(merged['components_available'].value_counts().sort_index())

print("\nOverall index stats:")
print(merged['slowdown_risk_index'].describe())