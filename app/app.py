import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

st.set_page_config(page_title="India Economic Slowdown Monitor", layout="wide", page_icon="📉")

# --- Custom CSS for finance-terminal feel ---
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { font-family: 'Courier New', monospace; letter-spacing: 0.5px; }
    h1 { color: #D4AF37; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    [data-testid="stMetric"] {
        background-color: #1A1F2B;
        border: 1px solid #2A2F3B;
        border-radius: 6px;
        padding: 15px;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Courier New', monospace;
        color: #D4AF37;
    }
    [data-testid="stMetricLabel"] { color: #888; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #666; }
    div[data-testid="stExpander"] {
        background-color: #1A1F2B;
        border: 1px solid #2A2F3B;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- Matplotlib dark theme to match ---
plt.style.use('dark_background')
mpl.rcParams['figure.facecolor'] = '#0E1117'
mpl.rcParams['axes.facecolor'] = '#0E1117'
mpl.rcParams['savefig.facecolor'] = '#0E1117'
mpl.rcParams['axes.edgecolor'] = '#333'
mpl.rcParams['grid.color'] = '#222'
mpl.rcParams['text.color'] = '#E8E8E8'
mpl.rcParams['axes.labelcolor'] = '#E8E8E8'
mpl.rcParams['xtick.color'] = '#888'
mpl.rcParams['ytick.color'] = '#888'

GOLD = '#D4AF37'
RISK_RED = '#C0392B'
GOOD_GREEN = '#2ECC71'
GREY = '#555'

# --- Load data ---
df = pd.read_csv("data/clean/slowdown_risk_index.csv", parse_dates=['date'])
gdp = pd.read_csv("data/clean/gdp_clean.csv")

st.title("INDIAN ECONOMIC SLOWDOWN MONITOR")
st.caption("A composite risk index built from CPI · IIP · Forex Reserves · USD-INR  —  not an official recession indicator")

st.markdown("<br>", unsafe_allow_html=True)

# --- Current reading ---
latest = df.iloc[-1]
components = int(latest['components_available'])
score = latest['slowdown_risk_index']

col1, col2, col3, col4 = st.columns(4)
col1.metric("SLOWDOWN RISK SCORE", f"{score:+.2f}")
col2.metric("AS OF", latest['date'].strftime("%b %Y").upper())
col3.metric("INDICATORS ACTIVE", f"{components}/4")

if score > 1.0:
    status, color = "ELEVATED", RISK_RED
elif score > 0.3:
    status, color = "WATCH", GOLD
else:
    status, color = "CALM", GOOD_GREEN
col4.markdown(f"""
    <div style="background-color:#1A1F2B;border:1px solid #2A2F3B;border-radius:6px;padding:15px;">
        <span style="color:#888;font-size:0.8rem;">STATUS</span><br>
        <span style="color:{color};font-family:'Courier New',monospace;font-size:1.6rem;font-weight:bold;">{status}</span>
    </div>
""", unsafe_allow_html=True)

if components <= 2:
    st.markdown(f"""
        <div style="background-color:#2B1F1A;border-left:4px solid {GOLD};padding:10px 15px;border-radius:4px;margin-top:15px;">
        ⚠️ <b>Low-confidence reading</b> — only {components}/4 indicators available this month. Treat with caution.
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Main chart ---
st.subheader("RISK INDEX — HISTORICAL")

fig, ax = plt.subplots(figsize=(14, 5))
high_conf = df['components_available'] >= 3
ax.plot(df['date'], df['slowdown_risk_index'], color=GOLD, linewidth=1.3, zorder=1, alpha=0.9)
ax.scatter(df.loc[high_conf, 'date'], df.loc[high_conf, 'slowdown_risk_index'], c=GOLD, s=10, zorder=2)
ax.scatter(df.loc[~high_conf, 'date'], df.loc[~high_conf, 'slowdown_risk_index'], c=GREY, s=10, zorder=2)
ax.axhline(0, color='#444', linestyle='--', linewidth=0.8)

events = [
    ("Taper Tantrum", "2013-05-01", "2013-09-01"),
    ("Demonetization", "2016-11-01", "2017-03-01"),
    ("COVID-19", "2020-03-01", "2020-09-01"),
]
for label, start, end in events:
    ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color=RISK_RED, alpha=0.15)
    ax.text(pd.Timestamp(start), ax.get_ylim()[1]*0.92, f" {label}", fontsize=8, color='#999', rotation=90, va='top')

ax.set_ylabel("Risk Score (z-avg)", color='#888')
ax.grid(axis='y', alpha=0.2)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
st.pyplot(fig)
st.caption("● Gold = full-confidence reading (3-4 indicators)   ● Grey = low-confidence reading (1-2 indicators)")

st.markdown("<br>", unsafe_allow_html=True)

# --- GDP annual chart ---
st.subheader("GDP GROWTH — ANNUAL")
st.caption("Shown separately from the monthly index, since GDP data only updates once a year.")
fig2, ax2 = plt.subplots(figsize=(14, 3))
gdp_years = gdp['Year'].str.replace('YR', '').astype(int)
bar_colors = [GOOD_GREEN if v >= 0 else RISK_RED for v in gdp['GDP_Growth_%']]
ax2.bar(gdp_years, gdp['GDP_Growth_%'], color=bar_colors, width=0.6)
ax2.axhline(0, color='#444', linewidth=0.8)
ax2.set_ylabel("GDP Growth %", color='#888')
ax2.grid(axis='y', alpha=0.2)
for spine in ['top', 'right']:
    ax2.spines[spine].set_visible(False)
st.pyplot(fig2)

st.markdown("<br>", unsafe_allow_html=True)

# --- Indicator table ---
st.subheader("LATEST READINGS")
latest_row = df[['date', 'cpi_yoy_inflation', 'iip_growth_rate', 'forex_reserves_usd_mn', 'usdinr_rate']].tail(6).copy()
latest_row.columns = ['Date', 'CPI Inflation %', 'IIP Growth %', 'Forex Reserves (USD Mn)', 'USD-INR']
st.dataframe(latest_row.set_index('Date'), width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

# --- Limitations ---
with st.expander("⚠️  METHODOLOGY & LIMITATIONS"):
    st.markdown("""
    - **Not an official recession indicator.** India has no NBER-equivalent body — reference periods shown are analyst-identified, not government-declared.
    - **CPI base-year splice gap.** MoSPI's CPI base year changed (2012=100 → 2024=100). Inflation is masked for ~12 months around the transition due to lack of an official linking factor.
    - **Low-confidence months exist**, especially recent ones — flagged in grey on the chart above.
    - **The 2013 Taper Tantrum isn't clearly visible**, likely due to insufficient rolling-window history that early in the dataset.
    - **Low inflation is treated as always "good."** In reality, unusually low inflation (e.g. post-2016 demonetization) can itself signal stress — a known simplification.
    - **Equal-weighted index**, not statistically optimized — too few historical events to responsibly tune weights.
    - **GDP is annual**, shown separately to avoid implying false monthly precision.
    """)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Sources: MoSPI (CPI, IIP, PLFS) · RBI (Forex) · World Bank (GDP) · Yahoo Finance (USD-INR)")