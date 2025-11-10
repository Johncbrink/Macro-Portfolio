# Aggregate DTI from CSVs
# Reads FRED CSVs with columns DATE,VALUE and outputs four ratios as PNGs in charts/
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

DATA = Path("data")
OUT = Path("charts")
OUT.mkdir(exist_ok=True, parents=True)

files = {
    "TCMDO": DATA / "TCMDO.csv",
    "GDP": DATA / "GDP.csv",
    "CMDEBT": DATA / "CMDEBT.csv",
    "DSPI": DATA / "DSPI.csv",
    "BCSNSDODNS": DATA / "BCSNSDODNS.csv",
    "CP": DATA / "CP.csv",
}

def load_series(path: Path, name: str) -> pd.Series:
    df = pd.read_csv(path)
    # Handle FRED variants: DATE,VALUE or observation_date,value
    date_col = "DATE" if "DATE" in df.columns else "observation_date"
    value_col = "VALUE" if "VALUE" in df.columns else "value"
    s = pd.to_datetime(df[date_col])
    v = pd.to_numeric(df[value_col], errors="coerce")
    ser = pd.Series(v.values, index=s, name=name).dropna()
    return ser

def to_quarter_end(ser: pd.Series) -> pd.Series:
    # Use last observation of each quarter
    return ser.resample("Q").last()

def plot_ratio(series: pd.Series, title: str, filename: str):
    plt.figure()
    series.plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Ratio")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

# Load
series = {name: load_series(path, name) for name, path in files.items()}

# Align to quarter end
for k in series:
    series[k] = to_quarter_end(series[k])

CMDEBT = series["CMDEBT"]
DSPI = series["DSPI"]
BCSNSDODNS = series["BCSNSDODNS"]
CP = series["CP"]
TCMDO = series["TCMDO"]
GDP = series["GDP"]

# Ratios
household = (CMDEBT / DSPI).dropna()
corporate = (BCSNSDODNS / CP).dropna()
debt_to_gdp = (TCMDO / GDP).dropna()
private = ((CMDEBT + BCSNSDODNS) / (DSPI + CP)).dropna()

# Save
plot_ratio(household, "Household Debt-to-Income (CMDEBT/DSPI)", "aggregate_household_dti.png")
plot_ratio(corporate, "Corporate Debt-to-Income (BCSNSDODNS/CP)", "aggregate_corporate_dti.png")
plot_ratio(debt_to_gdp, "Debt-to-GDP (TCMDO/GDP)", "aggregate_debt_to_gdp.png")
plot_ratio(private, "Private-Sector Debt-to-Income ((CMDEBT+BCSNSDODNS)/(DSPI+CP))", "aggregate_private_dti.png")

print("Saved charts to", OUT)
