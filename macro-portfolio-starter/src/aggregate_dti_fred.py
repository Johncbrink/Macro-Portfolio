# Aggregate DTI (FRED-only)
# Pulls six FRED series and computes four ratios:
#   1) Household DTI: CMDEBT / DSPI
#   2) Corporate DTI: BCSNSDODNS / CP
#   3) Debt-to-GDP: TCMDO / GDP
#   4) Private-Sector DTI: (CMDEBT + BCSNSDODNS) / (DSPI + CP)
#
# Saves four PNG charts into charts/
# Design: matplotlib only, one chart per figure, quarterly end-of-period alignment.

import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

OUT = Path("charts")
OUT.mkdir(exist_ok=True, parents=True)

START = datetime(1960,1,1)

def q_eop(s: pd.Series) -> pd.Series:
    return s.resample("Q").last()

def save_line(series: pd.Series, title: str, ylabel: str, filename: str):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    series.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=160)
    plt.close(fig)

def main():
    # Fetch from FRED (monthly or quarterly; we will re-sample to quarterly EOP)
    TCMDO = pdr.DataReader("TCMDO", "fred", START)["TCMDO"]
    GDP = pdr.DataReader("GDP", "fred", START)["GDP"]
    CMDEBT = pdr.DataReader("CMDEBT", "fred", START)["CMDEBT"]
    DSPI = pdr.DataReader("DSPI", "fred", START)["DSPI"]
    BCSNSDODNS = pdr.DataReader("BCSNSDODNS", "fred", START)["BCSNSDODNS"]
    CP = pdr.DataReader("CP", "fred", START)["CP"]

    # Quarter-end
    series = {
        "TCMDO": q_eop(TCMDO),
        "GDP": q_eop(GDP),
        "CMDEBT": q_eop(CMDEBT),
        "DSPI": q_eop(DSPI),
        "BCSNSDODNS": q_eop(BCSNSDODNS),
        "CP": q_eop(CP),
    }

    # Ratios
    household = (series["CMDEBT"] / series["DSPI"]).dropna()
    corporate = (series["BCSNSDODNS"] / series["CP"]).dropna()
    debt_to_gdp = (series["TCMDO"] / series["GDP"]).dropna()
    private = ((series["CMDEBT"] + series["BCSNSDODNS"]) / (series["DSPI"] + series["CP"])).dropna()

    # Save charts
    save_line(household, "Household Debt-to-Income (CMDEBT/DSPI)", "Ratio", "aggregate_household_dti.png")
    save_line(corporate, "Corporate Debt-to-Income (BCSNSDODNS/CP)", "Ratio", "aggregate_corporate_dti.png")
    save_line(debt_to_gdp, "Debt-to-GDP (TCMDO/GDP)", "Ratio", "aggregate_debt_to_gdp.png")
    save_line(private, "Private-Sector Debt-to-Income ((CMDEBT+BCSNSDODNS)/(DSPI+CP))", "Ratio", "aggregate_private_dti.png")

    latest = {
        "household": household.dropna().iloc[-1],
        "corporate": corporate.dropna().iloc[-1],
        "debt_to_gdp": debt_to_gdp.dropna().iloc[-1],
        "private": private.dropna().iloc[-1],
    }
    print("Latest ratios (quarterly):", latest)

if __name__ == "__main__":
    main()
