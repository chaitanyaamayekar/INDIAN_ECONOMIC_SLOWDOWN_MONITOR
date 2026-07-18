# import pandas as pd

# # CPI old series — find headline "all items" group
# cpi_old = pd.read_csv("data/raw/cpi_old_series_raw.csv")
# print("CPI OLD — unique groups:", cpi_old['group'].unique())
# print("CPI OLD — unique subgroups:", cpi_old['subgroup'].unique())
# print("CPI OLD — unique sectors:", cpi_old['sector'].unique())
# print("CPI OLD — year range:", cpi_old['year'].min(), "-", cpi_old['year'].max())
# print("CPI OLD — unique years count:", cpi_old['year'].nunique())

# print("\n" + "="*50 + "\n")

# # CPI new series — same check
# cpi_new = pd.read_csv("data/raw/cpi_new_series_raw.csv")
# print("CPI NEW — unique divisions:", cpi_new['division'].unique())
# print("CPI NEW — unique groups:", cpi_new['group'].unique())
# print("CPI NEW — unique sectors:", cpi_new['sector'].unique())

# print("\n" + "="*50 + "\n")

# # PLFS — find the headline unemployment measure
# plfs = pd.read_csv("data/raw/plfs_raw.csv")
# # print("PLFS — unique weekly_status:", plfs['weekly_status'].unique())
# plfs_clean = plfs[plfs['weekly_status'] == 'PS+SS']
# print("PLFS — unique employee_contract:", plfs['employee_contract'].unique())
# print("PLFS — unique sector:", plfs['sector'].unique())
# print("PLFS — unique AgeGroup:", plfs['AgeGroup'].unique())

# import pandas as pd
# iip = pd.read_csv("data/raw/iip_raw.csv")
# print("Unique years in raw IIP data:", sorted(iip['year'].unique()))
# print("Row count per year:")
# print(iip['year'].value_counts().sort_index())
# import esankhyiki
# meta = esankhyiki.get_metadata("IIP", base_year="2011-12", frequency="Monthly")
# print(meta)
# import pandas as pd
# cpi_old = pd.read_csv("data/raw/cpi_old_series_raw.csv")
# print(cpi_old['month'].value_counts())
import pandas as pd
df = pd.read_csv("data/clean/slowdown_risk_index.csv", parse_dates=['date'])
window = df[(df['date'] >= '2016-06-01') & (df['date'] <= '2018-06-01')]
print(window[['date', 'z_cpi_inflation', 'z_iip_growth', 'z_forex', 'z_usdinr', 'slowdown_risk_index']])