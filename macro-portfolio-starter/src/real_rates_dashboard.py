# Real Policy Rate: Fed Funds minus CPI YoY
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

OUT = Path("charts")
OUT.mkdir(exist_ok=True, parents=True)

start = datetime(1970,1,1)
ff = pdr.DataReader("FEDFUNDS", "fred", start)          # monthly
cpi = pdr.DataReader("CPIAUCSL", "fred", start)         # monthly

cpi_yoy = cpi.pct_change(12) * 100.0                    # YoY %
df = pd.concat([ff["FEDFUNDS"], cpi_yoy["CPIAUCSL"]], axis=1).dropna()
df.columns = ["FedFunds", "CPI_YoY"]
df["RealPolicyRate"] = df["FedFunds"] - df["CPI_YoY"]

plt.figure()
df["RealPolicyRate"].plot()
plt.title("Real Policy Rate = Fed Funds – CPI YoY")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.tight_layout()
plt.savefig(OUT / "real_policy_rate.png", dpi=160)
plt.close()

print("Saved charts/real_policy_rate.png")
