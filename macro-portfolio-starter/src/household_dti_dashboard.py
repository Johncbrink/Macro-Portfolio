# Household Debt-to-Income Dashboard (FRED)
# - Fetches Household Credit Market Debt (CMDEBT) and Disposable Personal Income (DSPI)
# - Converts to quarterly end-of-period
# - Produces 5 clean charts saved to charts/
#
# Charts:
#   1) household_dti.png                -- CMDEBT / DSPI
#   2) household_debt_level.png         -- CMDEBT level
#   3) household_income_level.png       -- DSPI level
#   4) household_dti_yoy.png            -- YoY % change of DTI
#   5) household_dti_percentile.png     -- Rolling percentile (entire history)
#
# Notes:
# - Uses matplotlib only (no seaborn/colors), one figure per chart
# - Recession shading via USREC
# - Designed for employer-friendly presentation

import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

OUT = Path("charts")
OUT.mkdir(exist_ok=True, parents=True)

START = datetime(1960,1,1)

def q_eop(s: pd.Series) -> pd.Series:
    # End-of-period quarterly
    return s.resample("Q").last()

def add_recession_shading(ax, rec: pd.Series):
    in_rec = False
    start_rec = None
    for date, val in rec.items():
        if val == 1 and not in_rec:
            in_rec = True
            start_rec = date
        elif val == 0 and in_rec:
            in_rec = False
            ax.axvspan(start_rec, date, alpha=0.15)

    if in_rec:
        ax.axvspan(start_rec, rec.index[-1], alpha=0.15)

def save_line(series: pd.Series, title: str, ylabel: str, filename: str, rec_q: pd.Series = None):
    fig, ax = plt.subplots()
    series.plot(ax=ax)
    if rec_q is not None:
        add_recession_shading(ax, rec_q)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=160)
    plt.close(fig)

def main():
    # Fetch monthly series
    cmdebt = pdr.DataReader("CMDEBT", "fred", START)["CMDEBT"]
    dspi   = pdr.DataReader("DSPI", "fred", START)["DSPI"]
    usrec  = pdr.DataReader("USREC", "fred", START)["USREC"]

    # Quarterly EOP
    cm_q = q_eop(cmdebt)
    di_q = q_eop(dspi)
    rec_q = q_eop(usrec).dropna()

    # Align
    df = pd.concat([cm_q, di_q], axis=1).dropna()
    df.columns = ["CMDEBT", "DSPI"]
    df["DTI"] = df["CMDEBT"] / df["DSPI"]

    # YoY of DTI (quarterly)
    dti_yoy = df["DTI"].pct_change(4) * 100.0

    # Entire-history percentile for DTI
    # Percentile p_t = rank(DTI_t) / N * 100
    ranks = df["DTI"].rank(method="average")
    percentile = ranks / ranks.max() * 100.0

    # Save charts
    save_line(df["DTI"], "Household Debt-to-Income (CMDEBT / DSPI)", "Ratio", "household_dti.png", rec_q)
    save_line(df["CMDEBT"], "Household Credit Market Debt (CMDEBT)", "Billions USD", "household_debt_level.png", rec_q)
    save_line(df["DSPI"], "Disposable Personal Income (DSPI)", "Billions USD", "household_income_level.png", rec_q)
    save_line(dti_yoy.dropna(), "Household DTI — YoY Change", "Percent", "household_dti_yoy.png", rec_q)
    save_line(percentile, "Household DTI — Historical Percentile", "Percentile (0–100)", "household_dti_percentile.png", rec_q)

    # Text output for quick terminal context
    latest = df.dropna().iloc[-1]
    print("Latest quarter:")
    print(latest)
    print("Latest DTI YoY (%):", dti_yoy.dropna().iloc[-1])
    print("Latest DTI Percentile:", percentile.iloc[-1])

if __name__ == "__main__":
    main()
