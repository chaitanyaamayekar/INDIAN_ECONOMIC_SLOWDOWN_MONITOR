import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/clean/slowdown_risk_index.csv", parse_dates=['date'])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df['date'], df['slowdown_risk_index'], color='steelblue', linewidth=1.5)
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)

# Shade known slowdown periods
events = [
    ("2013 Taper Tantrum", "2013-05-01", "2013-09-01"),
    ("2016-17 Demonetization", "2016-11-01", "2017-03-01"),
    ("2020 COVID", "2020-03-01", "2020-09-01"),
]
for label, start, end in events:
    ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color='red', alpha=0.15)
    ax.text(pd.Timestamp(start), ax.get_ylim()[1]*0.9, label, fontsize=8, rotation=90, va='top')

ax.set_title("India Economic Slowdown Risk Index (2013-2026)")
ax.set_ylabel("Composite Risk Score (z-score avg)")
plt.tight_layout()
plt.savefig("data/clean/slowdown_index_backtest.png", dpi=150)
plt.show()
print("Chart saved to data/clean/slowdown_index_backtest.png")