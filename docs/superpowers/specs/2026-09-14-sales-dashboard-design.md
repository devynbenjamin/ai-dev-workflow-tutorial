# Design: ShopSmart Sales Dashboard

Source: `prd/ecommerce-analytics.md`
Tracked milestones: `TASKS.md` (TASK-1 through TASK-7)

## Summary

A single-page Streamlit dashboard reading `data/sales-data.csv` and
displaying two KPIs, a monthly sales trend line chart, and category/region
bar charts, per PRD Phase 1 scope (FR-1 through FR-5). Deployment to
Streamlit Community Cloud (M7 / TASK-7) is out of scope for the
implementation plan and is called out as a manual, user-executed step.

## Decisions from clarifying questions

- **Trend granularity**: monthly (12 points), not daily. Matches the PRD's
  own example axis labels (Jan, Feb, Mar...) and gives a cleaner line for
  an executive audience than 365 daily points.
- **Error handling**: minimal. The CSV is a known, fixed file matching the
  PRD's documented schema, not user-uploaded input — so `load_data()` does
  not add schema/type validation beyond what `pandas.read_csv` does by
  default. This keeps the calculations module small and readable.
- **Test fixtures**: hand-crafted, in-memory DataFrames with hand-computed
  expected values, not the real `sales-data.csv`. Keeps tests fast and
  independent of the shipped data file changing later.
- **Dashboard title**: "ShopSmart Sales Dashboard" — matches the company
  name used throughout the PRD's prose. (The PRD's own ASCII mockup reads
  "SHOPMART SALES DASHBOARD," which appears to be a typo against the
  company name "ShopSmart" used everywhere else in the document.)
- **Bar chart orientation**: vertical bars, matching the PRD's mockup,
  for an easier "biggest to smallest" read at a glance.

## Architecture

```
app.py                        # Streamlit UI: page config, layout, charts
sales_calculations.py         # Pure functions: load + aggregate, no UI imports
tests/
  test_sales_calculations.py  # pytest, hand-crafted fixture DataFrames
data/sales-data.csv           # existing, per PRD Data Specification
requirements.txt              # exact-pinned dependencies
venv/                         # local virtualenv, not committed
```

**Data flow**: `app.py` calls `sales_calculations.load_data(path)` once at
startup to get a DataFrame, then passes that DataFrame into small
aggregation functions. Each aggregation function takes a DataFrame in and
returns a plain value or DataFrame out — no Streamlit imports inside
`sales_calculations.py`, no hidden state. This is what makes the module
independently unit-testable with pytest, without importing or running
Streamlit at all. Plotly figure construction stays in `app.py`, not in
the calculations module, so that module stays purely about arithmetic
correctness (sums, counts, group-bys) — never about presentation.

## `sales_calculations.py` — function inventory

| Function | Input | Output | Maps to |
|---|---|---|---|
| `load_data(path)` | CSV path | DataFrame | FR-5 |
| `total_sales(df)` | DataFrame | float | FR-1 |
| `total_orders(df)` | DataFrame | int | FR-1 |
| `monthly_trend(df)` | DataFrame | DataFrame (month, sales) | FR-2 |
| `sales_by_category(df)` | DataFrame | DataFrame (category, sales), sorted desc | FR-3 |
| `sales_by_region(df)` | DataFrame | DataFrame (region, sales), sorted desc | FR-4 |

## UI layout (`app.py`)

Top to bottom, matching the PRD's mockup:

1. `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")`
   and `st.title(...)`.
2. KPI row: `st.columns(2)`, each an `st.metric()` — Total Sales formatted
   as currency with comma separators (e.g. `$116,500`), Total Orders as a
   plain formatted count (e.g. `482`).
3. Trend chart: full-width `px.line` (Plotly Express), monthly x-axis,
   rendered via `st.plotly_chart(fig, use_container_width=True)`. Plotly's
   default hover tooltips satisfy FR-2's interactivity requirement with no
   extra code.
4. Category & region row: `st.columns(2)`, each a vertical `px.bar`,
   sorted descending by sales value, satisfying FR-3/FR-4.

Plotly Express is used throughout (rather than building charts manually)
because its defaults — hover tooltips, axis labels, legends — satisfy
NFR-2 (no training required, clear labels) essentially for free, which is
also why the PRD's own Technical Approach section recommends it.

## Testing strategy

`tests/test_sales_calculations.py` builds one small in-memory DataFrame
(4-6 rows spanning at least 2 categories, 2 regions, and 2 months) with
hand-computed expected totals, then asserts each function in
`sales_calculations.py` against those known values.

No automated tests target `app.py` — Streamlit UI code isn't meaningfully
unit-testable here. The PRD's acceptance criteria (no errors, correct
values, professional appearance) are verified by actually running the app
locally (`streamlit run app.py`), which is the Definition of Done's
explicit runtime check and TASK-6's purpose.

## Dependencies

`requirements.txt` pins exact versions (`streamlit==X.Y.Z`,
`plotly==X.Y.Z`, `pandas==X.Y.Z`, `pytest==X.Y.Z`), captured from whatever
installs cleanly into a plain `venv/` virtual environment during TASK-1.
Exact pins keep the environment reproducible for a single-contributor,
single-deployment-target project — there's no reason to allow a version
range here.

## Out of scope

- Everything in the PRD's Phase 2 (auth, DB integration, export, alerts,
  filtering, drill-down, mobile responsiveness) — explicitly out of scope
  per the PRD.
- Deployment to Streamlit Community Cloud (PRD milestone M7 / TASK-7):
  the implementation plan stops after local verification (TASK-6) and
  hands off to the user, who deploys manually from `main` after merging
  this feature branch.
