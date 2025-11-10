# Macro Portfolio — Starter Dashboards

This repo is a clean, employer‑friendly starting point for your macro dashboards. It follows a simple structure and produces publishable charts saved into `charts/`.

## Projects included
1. **Aggregate DTI (CSV)** — Household, Corporate, Debt‑to‑GDP, Private‑Sector (reads your local FRED CSVs).
2. **Yield Curve (FRED)** — 10y–2y spread with NBER recession shading (fetches directly from FRED).
3. **Real Policy Rate (FRED)** — Fed Funds minus CPI YoY (and vs nominal GDP growth if desired).

4. **Household DTI (FRED)** — CMDEBT / DSPI with YoY and historical percentile.

### New: Household DTI (FRED-only)
```bash
python3 src/household_dti_dashboard.py
# outputs charts/household_dti*.png
```


> Design: clean matplotlib defaults, quarter‑end alignment, exported PNGs for resumes/notes.

## Setup (GitHub Codespaces)
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Run
```bash
# From repo root
python3 src/aggregate_dti_from_csv.py       # saves charts/aggregate_*.png
python3 src/yield_curve_dashboard.py        # saves charts/yield_curve_10y_2y.png
python3 src/real_rates_dashboard.py         # saves charts/real_policy_rate.png
```

## Research Notes

Use `notes/Bottom80_DTI_Note_template.md` or create new notes per project, export to PDF, and commit both PNG and PDF.

## Publish
```bash
git add .
git commit -m "Add macro dashboards and notes"
git push
```


### Aggregate DTI (FRED-only)
```bash
python3 src/aggregate_dti_fred.py
# outputs charts/aggregate_*.png
```
