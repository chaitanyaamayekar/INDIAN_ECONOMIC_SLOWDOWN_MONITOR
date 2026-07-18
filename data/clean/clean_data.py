import pandas as pd

# ============================================================
# 1. CPI — splice old (2013-2024) + new (2025-2026) series
# ============================================================
cpi_old = pd.read_csv("data/raw/cpi_old_series_raw.csv")
cpi_new = pd.read_csv("data/raw/cpi_new_series_raw.csv")

month_map = {
    'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
    'July':7,'August':8,'September':9,'October':10,'November':11,'December':12
}
cpi_old['month_num'] = cpi_old['month'].map(month_map)
cpi_old['date'] = pd.to_datetime(dict(year=cpi_old['year'], month=cpi_old['month_num'], day=1))
cpi_old_clean = cpi_old[['date', 'index']].rename(columns={'index': 'cpi_index'}).sort_values('date')

cpi_new_filtered = cpi_new[(cpi_new['division'] == 'CPI (General)') & (cpi_new['sector'] == 'Combined')].copy()
cpi_new_filtered['month_num'] = cpi_new_filtered['month'].map(month_map)
cpi_new_filtered['date'] = pd.to_datetime(dict(year=cpi_new_filtered['year'], month=cpi_new_filtered['month_num'], day=1))
cpi_new_clean = cpi_new_filtered[['date', 'index']].rename(columns={'index': 'cpi_index'}).sort_values('date')

cpi_combined = pd.concat([
    cpi_old_clean[['date', 'cpi_index']],
    cpi_new_clean[['date', 'cpi_index']]
], ignore_index=True).sort_values('date').drop_duplicates('date')

cpi_combined.to_csv("data/clean/cpi_clean.csv", index=False)
print(f"CPI clean: {len(cpi_combined)} rows, {cpi_combined['date'].min()} to {cpi_combined['date'].max()}")
# ============================================================
# 2. IIP — filter to General category
# ============================================================
iip = pd.read_csv("data/raw/iip_raw.csv")
iip_general = iip[iip['category'] == 'General'].copy()  # keep as safety check

iip_general['month_num'] = iip_general['month'].map(month_map)
iip_general['date'] = pd.to_datetime(dict(
    year=iip_general['year'],
    month=iip_general['month_num'],
    day=1
))
iip_general = iip_general.drop_duplicates('date')

iip_clean = iip_general[['date', 'index', 'growth_rate']].rename(
    columns={'index': 'iip_index', 'growth_rate': 'iip_growth_rate'}
).sort_values('date')
iip_clean.to_csv("data/clean/iip_clean.csv", index=False)
print(f"IIP clean: {len(iip_clean)} rows, {iip_clean['date'].min()} to {iip_clean['date'].max()}")

# ============================================================
# 3. PLFS — filter to headline unemployment measure (PS+SS)
# ============================================================
# plfs = pd.read_csv("data/raw/plfs_raw.csv")
# plfs_headline = plfs[plfs['weekly_status'] == 'PS+SS'].copy()
# plfs_headline['start_year'] = plfs_headline['year'].str.split('-').str[0].astype(int)
# plfs_headline['date'] = pd.to_datetime(plfs_headline['start_year'].astype(str) + '-04-01')
# plfs_clean = plfs_headline[['date', 'value']].rename(columns={'value': 'unemployment_rate'}).sort_values('date')
# plfs_clean.to_csv("data/clean/plfs_clean.csv", index=False)
# print(f"PLFS clean: {len(plfs_clean)} rows")
plfs = pd.read_csv("data/raw/plfs_raw.csv")
plfs_headline = plfs[
    (plfs['weekly_status'] == 'PS+SS') &
    (plfs['religion'] == 'all') &
    (plfs['socialGroup'] == 'all') &
    (plfs['General_Education'] == 'all')
].copy()

plfs_headline['start_year'] = plfs_headline['year'].str.split('-').str[0].astype(int)
plfs_headline['date'] = pd.to_datetime(plfs_headline['start_year'].astype(str) + '-04-01')
plfs_clean = plfs_headline[['date', 'value']].rename(columns={'value': 'unemployment_rate'}).sort_values('date')
plfs_clean.to_csv("data/clean/plfs_clean.csv", index=False)
print(f"PLFS clean: {len(plfs_clean)} rows")
print(plfs_clean)

# ============================================================
# 4. Forex reserves
# ============================================================
forex = pd.read_csv("data/raw/forex_reserves_raw.csv")
forex['month_num'] = forex['month'].map(month_map)
forex['date'] = pd.to_datetime(dict(year=forex['year'], month=forex['month_num'], day=1))
forex_clean = forex[['date', 'value']].rename(columns={'value': 'forex_reserves_usd_mn'}).sort_values('date')
forex_clean.to_csv("data/clean/forex_clean.csv", index=False)
print(f"Forex clean: {len(forex_clean)} rows")

# ============================================================
# 5. USD-INR — resample daily to monthly average
# ============================================================
inr = pd.read_csv("data/raw/usdinr_raw.csv")
inr['Date'] = pd.to_datetime(inr['Date'])
inr_monthly = inr.set_index('Date')['Close'].resample('MS').mean().reset_index()
inr_monthly.columns = ['date', 'usdinr_rate']
inr_monthly.to_csv("data/clean/usdinr_clean.csv", index=False)
print(f"USD-INR clean: {len(inr_monthly)} rows")

# ============================================================
# 6. GDP — kept separate, annual, not merged into main index
# ============================================================
gdp = pd.read_csv("data/raw/gdp_worldbank_raw.csv")
gdp.to_csv("data/clean/gdp_clean.csv", index=False)
print(f"GDP clean: {len(gdp)} rows (kept separate, annual)")

# ============================================================
# 7. Merge monthly/quarterly indicators into one aligned table
# ============================================================

merged = cpi_combined.merge(iip_clean, on='date', how='outer') \
                      .merge(forex_clean, on='date', how='outer') \
                      .merge(inr_monthly, on='date', how='outer') \
                      .sort_values('date')
merged = merged.set_index('date')
merged['cpi_yoy_inflation'] = merged['cpi_index'].pct_change(periods=12, freq='MS') * 100
merged = merged.reset_index()
# After computing cpi_yoy_inflation, mask out cross-series comparisons
new_series_start = cpi_new_clean['date'].min()  # should be 2025-01-01 or similar
splice_invalid_end = new_series_start + pd.DateOffset(months=11)  # first 12 months of new series

merged.loc[
    (merged['date'] >= new_series_start) & (merged['date'] <= splice_invalid_end),
    'cpi_yoy_inflation'
] = pd.NA

print(f"Masked cpi_yoy_inflation as NaN from {new_series_start.date()} to {splice_invalid_end.date()} — base-year splice, no valid YoY comparison possible without MOSPI's linking factor")

# Trim to 2013 onward — right here, AFTER merged is created
merged = merged[merged['date'] >= '2013-01-01'].reset_index(drop=True)

merged.to_csv("data/clean/merged_indicators.csv", index=False)
print(f"Merged dataset (trimmed): {len(merged)} rows, {merged['date'].min()} to {merged['date'].max()}")
print(merged.head(10))
print(merged.tail(10))