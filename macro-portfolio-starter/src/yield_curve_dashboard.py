# Yield Curve 10y-2y with recession shading
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

OUT = Path("charts")
OUT.mkdir(exist_ok=True, parents=True)

start = datetime(1970,1,1)
d10 = pdr.DataReader("DGS10", "fred", start)
d2 = pdr.DataReader("DGS2", "fred", start)
rec = pdr.DataReader("USREC", "fred", start)

spread = (d10["DGS10"] - d2["DGS2"]).dropna()
df = pd.concat([spread, rec["USREC"]], axis=1).dropna()
df.columns = ["spread_10y_2y", "USREC"]

plt.figure()
df["spread_10y_2y"].plot()
# Shade recessions
in_rec = False
start_rec = None
for date, val in df["USREC"].items():
    if val == 1 and not in_rec:
        in_rec = True
        start_rec = date
    elif val == 0 and in_rec:
        in_rec = False
        plt.axvspan(start_rec, date, alpha=0.2)
# If currently in recession:
if in_rec:
    plt.axvspan(start_rec, df.index[-1], alpha=0.2)

plt.title("Yield Curve: 10y–2y (FRED) with Recessions")
plt.xlabel("Date")
plt.ylabel("Percentage Points")
plt.tight_layout()
plt.savefig(OUT / "yield_curve_10y_2y.png", dpi=160)
plt.close()
print("Saved charts/yield_curve_10y_2y.png")
