🇮🇳 India Economic Slowdown Monitor

A composite economic slowdown risk index for India, built from four public macroeconomic indicators — CPI inflation, industrial production (IIP), forex reserves, and the USD-INR exchange rate — tracked monthly from 2013 to present.

Live dashboard: https://indias-economicslowdownmonitor.streamlit.app/


What this is

Instead of relying on a black-box recession model or importing a US-style framework wholesale, this project builds a transparent, from-first-principles risk index using official Indian government data (MoSPI, RBI) and the World Bank.

Each indicator is:


Converted to a rolling 3-year z-score (how unusual is this value relative to its own recent history)
Sign-adjusted so "higher always means more risk," regardless of which direction the raw indicator moves
Averaged into a single composite score


Important framing note: India has no official recession-dating body, unlike the US's NBER. That's why this project is deliberately called a "Slowdown Risk" monitor, not a "Recession" monitor — and why the reference periods below are analyst-identified historical stress events, not officially declared recessions.


Key finding

The index shows a clear, visible spike around the 2016-17 Demonetization period and an even sharper spike during 2020 COVID — its two most severe, unambiguous shocks. It does not show a clear signal for the 2013 Taper Tantrum, most likely because the rolling z-score window doesn't yet have enough historical data to work with that early in the series.

A closer look at the months following demonetization also revealed a real methodological limitation: the index briefly reads as "low risk" right after the event, because inflation dropped sharply due to a genuine cash-supply shock — and the model currently treats any drop in inflation as automatically good. In reality, unusually low inflation can itself be a sign of economic stress. This is discussed further below.


Data sources

IndicatorSourceAccess methodCPI InflationMinistry of Statistics and Programme Implementation (MoSPI)Official mospi-esankhyiki Python clientIndustrial Production (IIP)MoSPImospi-esankhyikiUnemployment (PLFS)MoSPImospi-esankhyikiForex ReservesReserve Bank of India (RBI)mospi-esankhyiki (RBI dataset)GDP Growth (annual)World Bank Open DatawbgapiUSD-INR Exchange RateYahoo Financeyfinance


Methodology


Fetch raw data from each source via their respective APIs
Clean — filter to national headline figures only (e.g., "All India," "Combined" sector, "General" category), removing regional and sub-category breakdowns
Align — resample and merge everything into one common monthly calendar
Feature engineer — compute a rolling 3-year (36-month) z-score per indicator, using a minimum 12-month window to allow the index to begin before a full 3 years of history exists
Sign-adjust — flip indicators where "higher is good" (IIP growth, forex reserves) so that every component consistently means "higher = more risk"
Combine — average all available components into one composite Slowdown Risk Index per month
Flag confidence — track how many of the 4 indicators contributed to each month's score, since some months have incomplete data


GDP growth is tracked and displayed separately as an annual chart, rather than blended into the monthly index, since forward-filling an annual figure into monthly data would imply false precision.


Limitations — read before trusting this

This project is a portfolio/educational tool, not a financial or policy instrument. Specific known limitations:


Not an official recession indicator. No government body officially dates Indian recessions. Reference periods (2013, 2016-17, 2020) are analyst-identified, not government-declared.
CPI has an unresolved base-year splice gap. MoSPI changed CPI's base year from 2012=100 to 2024=100 in 2025. Since no official linking factor was applied, year-over-year inflation is masked (left blank) for the ~12 months where the comparison would span both series, rather than showing a mathematically invalid number.
The 2013 Taper Tantrum isn't clearly visible in the index, most likely due to insufficient rolling-window history that early in the dataset (fewer than 36 months of prior data available).
Low inflation is scored as always "good." In reality, unusually low inflation can itself signal economic stress (as seen after 2016 demonetization). A more advanced version of this index would score CPI's distance from "normal" in both directions, not just flag high inflation as risk.
Equal-weighted, not statistically optimized. All four indicators contribute equally to the composite score. This is a deliberate simplification — there are only 3-4 major historical events to validate against, which isn't enough data to responsibly fit optimized weights without overfitting.
Low-confidence months exist, particularly recent months, where fewer than 3 of 4 indicators are available due to normal government publishing lag or the CPI splice masking. These are flagged in grey on the dashboard chart and should be read with caution — especially the most recent 1-2 months.
PLFS (unemployment) data only exists from 2017-18 onward and is not included in the composite index due to its annual (not monthly) frequency — shown for reference only.
GDP is annual, shown as a separate chart, not blended into the monthly composite index.



Running locally

bashgit clone https://github.com/YOUR-USERNAME/indian_economic_slowdown_monitor.git
cd indian_economic_slowdown_monitor
pip install -r requirements.txt
streamlit run app/app.py

Refreshing the data

The deployed dashboard reads from static CSV snapshots — it does not fetch live data on every visit. To refresh the underlying data:

bashpython data/raw/fetch_data.py       # pulls latest raw data from all sources
python data/clean/clean_data.py     # cleans and merges into one dataset
python data/build_index.py          # recomputes z-scores and the composite index

Refreshing requires the data-pipeline packages (esankhyiki, wbgapi, yfinance), which are not included in requirements.txt since the deployed app itself only needs streamlit, pandas, numpy, and matplotlib to read the pre-built CSVs. Install the pipeline packages separately if you want to refresh the data yourself:

pip install esankhyiki wbgapi yfinance

Update frequency by indicator (due to how each source publishes):


USD-INR: near real-time
Forex Reserves: weekly
CPI, IIP: monthly, with ~2-6 week publishing lag
PLFS, GDP: annual

Project structure
india-econ-monitor/
├── app/
│   └── app.py                 # Streamlit dashboard
├── data/
│   ├── raw/                   # Raw fetched data from APIs
│   └── clean/                 # Cleaned, merged, and index-ready datasets
├── .streamlit/
│   └── config.toml            # Dashboard theme
├── fetch_data.py               # Data ingestion from MoSPI, RBI, World Bank, Yahoo Finance
├── clean_data.py                # Cleaning, filtering, and merging pipeline
├── build_index.py               # Z-score feature engineering and composite index
├── requirements.txt
└── README.md

Acknowledgements

Built using the official MoSPI mospi-esankhyiki Python client, the World Bank's public API via wbgapi, and yfinance.