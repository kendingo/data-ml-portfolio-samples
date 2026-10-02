# Data and ML portfolio samples

Small, self-contained examples of the Python and SQL I use day to day in analytics and data engineering. All data is synthetic. These are sample projects written for this portfolio, not code from any employer.

| File | What it shows |
|------|---------------|
| `churn_propensity.py` | Feature engineering and a baseline churn propensity model (logistic regression) with AUC and top-decile lift |
| `data_quality_checks.py` | Data quality checks on an events table: nulls, duplicates, late arrivals, unexpected event names |
| `bigquery_cost_audit.sql` | Finding the most expensive BigQuery queries to guide cost optimisation (partitioning, clustering, column pruning) |

## Run

```bash
pip install -r requirements.txt
python churn_propensity.py
python data_quality_checks.py
```

Author: Ken Kuyoh, London. Founder of SignFlow Now.
