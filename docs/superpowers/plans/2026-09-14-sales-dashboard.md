# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 Streamlit sales dashboard (KPIs, trend chart, category/region breakdowns) described in `prd/ecommerce-analytics.md`.

**Architecture:** A single Streamlit page (`app.py`) reads a DataFrame once via `sales_calculations.load_data()`, then renders KPIs and Plotly charts built from small pure aggregation functions in `sales_calculations.py`. The calculations module has no Streamlit or Plotly imports, so it can be unit-tested with pytest in isolation.

**Tech Stack:** Python 3.11+, Streamlit, Plotly Express, Pandas, pytest — plain `venv/` virtual environment, exact-pinned `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-14-sales-dashboard-design.md`

## Numbering note

This plan's own steps are labeled **"Plan Step 1"** through **"Plan Step 7"**.
Each Plan Step is separately tagged with the `TASKS.md` milestone it
implements (`TASK-1` through `TASK-7`). The two numbering schemes are
intentionally distinct — do not conflate "Plan Step 3" with "TASK-3" in
prose; always use the full label.

## Global Constraints

- Work directly on the current git branch (`feature/sales-dashboard`) — do not create a git worktree.
- Use a plain Python virtual environment at `venv/` (`python3 -m venv venv`) — no `uv`, no `conda`. `venv/` is not committed.
- Pin exact dependency versions in `requirements.txt` (`streamlit`, `pandas`, `plotly`, `pytest`) — captured from what installs cleanly, not hand-guessed version numbers.
- `sales_calculations.py` contains only pure data functions: no Streamlit imports, no Plotly/chart-building code.
- Every function in `sales_calculations.py` is unit-tested in `tests/test_sales_calculations.py` using hand-crafted fixtures (in-memory DataFrames, or a small temp CSV for `load_data`) — never the real `data/sales-data.csv`.
- Dashboard title text is exactly `"ShopSmart Sales Dashboard"` (the PRD mockup's "SHOPMART" is treated as a typo against the company name used throughout the PRD).
- Trend chart uses monthly granularity, not daily.
- Bar charts are vertical, sorted descending by sales value.
- Minimal error handling: `data/sales-data.csv` is treated as a known, well-formed file — no schema/type validation beyond pandas' own CSV parsing.
- Code has no comments beyond what's already shown in this plan's code blocks — keep it simple and readable per the user's ground rules.
- Deployment (`TASK-7` / PRD milestone M7) is **not performed by this plan**. Plan Step 7 documents the steps but is explicitly the user's own manual action after merging to `main`.

---

### Plan Step 1 — Milestone: TASK-1 (Environment setup and project initialization)

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable `app.py` shell that later steps extend; the `venv/` environment and `requirements.txt` that all later steps rely on.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`

- [ ] **Step 2: Activate it and install dependencies**

Run:
```bash
source venv/bin/activate
pip install streamlit pandas plotly pytest
```

- [ ] **Step 3: Pin exact versions into requirements.txt**

Run: `pip freeze | grep -iE '^(streamlit|pandas|plotly|pytest)==' > requirements.txt`

Expected: `requirements.txt` now has four lines, each `package==X.Y.Z`.

- [ ] **Step 4: Create .gitignore**

```
venv/
__pycache__/
*.pyc
```

- [ ] **Step 5: Create app.py**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 6: Verify the app launches**

Run: `streamlit run app.py`
Expected: browser opens showing only the title "ShopSmart Sales Dashboard", no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .gitignore app.py
git commit -m "TASK-1: Set up project environment and app skeleton"
```

---

### Plan Step 2 — Milestone: TASK-2 (Data loading and basic structure)

**Files:**
- Create: `sales_calculations.py`
- Create: `tests/test_sales_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: nothing from Plan Step 1 beyond the installed dependencies.
- Produces: `load_data(path: str) -> pd.DataFrame`, with a `date` column already parsed to datetime — every later Plan Step's functions take this DataFrame as input.

- [ ] **Step 1: Write the failing test for load_data**

Create `tests/test_sales_calculations.py`:

```python
import pandas as pd

from sales_calculations import load_data


def test_load_data_reads_csv_with_parsed_dates(tmp_path):
    csv_content = (
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Widget,Electronics,North,2,10.00,20.00\n"
        "2024-01-04,ORD-002,Gadget,Accessories,South,1,15.00,15.00\n"
    )
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(csv_content)

    df = load_data(str(csv_path))

    assert len(df) == 2
    assert list(df.columns) == [
        "date", "order_id", "product", "category", "region",
        "quantity", "unit_price", "total_amount",
    ]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'sales_calculations'`

- [ ] **Step 3: Implement load_data**

Create `sales_calculations.py`:

```python
import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: PASS

- [ ] **Step 5: Wire load_data into app.py**

Modify `app.py`:

```python
import streamlit as st

from sales_calculations import load_data

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

df = load_data("data/sales-data.csv")
```

- [ ] **Step 6: Verify the app still runs**

Run: `streamlit run app.py`
Expected: same title-only page, no errors in the terminal (the loaded DataFrame isn't displayed yet). Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_calculations.py tests/test_sales_calculations.py app.py
git commit -m "TASK-2: Add CSV data loading"
```

---

### Plan Step 3 — Milestone: TASK-3 (KPI cards implementation)

**Files:**
- Modify: `sales_calculations.py`
- Modify: `tests/test_sales_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_data` from Plan Step 2.
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int` — not consumed by later Plan Steps, but establishes the `sample_df` pytest fixture that Plan Steps 4 and 5 reuse.

- [ ] **Step 1: Write the failing tests**

Modify `tests/test_sales_calculations.py` — change the import line:

```python
# before
from sales_calculations import load_data

# after
import pytest

from sales_calculations import load_data, total_sales, total_orders
```

Append to the end of the file:

```python
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-03", "2024-01-04", "2024-02-01", "2024-02-02"]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004"],
        "category": ["Electronics", "Accessories", "Electronics", "Audio"],
        "region": ["North", "South", "North", "East"],
        "total_amount": [20.00, 15.00, 30.00, 10.00],
    })


def test_total_sales_sums_all_transactions(sample_df):
    assert total_sales(sample_df) == 75.00


def test_total_orders_counts_rows(sample_df):
    assert total_orders(sample_df) == 4
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'total_sales'`

- [ ] **Step 3: Implement total_sales and total_orders**

Append to `sales_calculations.py`:

```python
def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Add the KPI row to app.py**

Modify `app.py`:

```python
import streamlit as st

from sales_calculations import load_data, total_sales, total_orders

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

df = load_data("data/sales-data.csv")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")
```

- [ ] **Step 6: Verify the KPIs render correctly**

Run: `streamlit run app.py`
Expected: two metric cards — Total Orders shows exactly `482` (per the PRD's Data Specification); Total Sales shows a dollar figure close to the PRD's ~$116,500 estimate, comma-separated with no decimals. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_calculations.py tests/test_sales_calculations.py app.py
git commit -m "TASK-3: Add KPI cards for total sales and total orders"
```

---

### Plan Step 4 — Milestone: TASK-4 (Sales trend chart)

**Files:**
- Modify: `sales_calculations.py`
- Modify: `tests/test_sales_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_data` from Plan Step 2, `sample_df` fixture from Plan Step 3.
- Produces: `monthly_trend(df: pd.DataFrame) -> pd.DataFrame` with columns `month` (str, `"YYYY-MM"`, chronologically sorted) and `total_amount` (float) — not consumed by later Plan Steps.

- [ ] **Step 1: Write the failing test**

Modify `tests/test_sales_calculations.py` — change the import line:

```python
# before
from sales_calculations import load_data, total_sales, total_orders

# after
from sales_calculations import load_data, total_sales, total_orders, monthly_trend
```

Append to the end of the file:

```python
def test_monthly_trend_groups_by_month_sorted_chronologically(sample_df):
    result = monthly_trend(sample_df)

    assert list(result["month"]) == ["2024-01", "2024-02"]
    assert list(result["total_amount"]) == [35.00, 40.00]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'monthly_trend'`

- [ ] **Step 3: Implement monthly_trend**

Append to `sales_calculations.py`:

```python
def monthly_trend(df):
    return (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Add the trend chart to app.py**

Modify `app.py`:

```python
import plotly.express as px
import streamlit as st

from sales_calculations import load_data, total_sales, total_orders, monthly_trend

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

df = load_data("data/sales-data.csv")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

trend = monthly_trend(df)
trend_fig = px.line(
    trend,
    x="month",
    y="total_amount",
    title="Monthly Sales Trend",
    labels={"month": "Month", "total_amount": "Sales ($)"},
    markers=True,
)
st.plotly_chart(trend_fig, use_container_width=True)
```

- [ ] **Step 6: Verify the trend chart renders**

Run: `streamlit run app.py`
Expected: a line chart below the KPIs with 12 monthly points, hovering a point shows its month and dollar value. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_calculations.py tests/test_sales_calculations.py app.py
git commit -m "TASK-4: Add monthly sales trend chart"
```

---

### Plan Step 5 — Milestone: TASK-5 (Category and region breakdowns)

**Files:**
- Modify: `sales_calculations.py`
- Modify: `tests/test_sales_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_data` from Plan Step 2, `sample_df` fixture from Plan Step 3.
- Produces: `sales_by_category(df) -> pd.DataFrame` and `sales_by_region(df) -> pd.DataFrame`, each with columns `category`/`region` and `total_amount`, sorted descending by `total_amount` — not consumed by later Plan Steps.

- [ ] **Step 1: Write the failing tests**

Modify `tests/test_sales_calculations.py` — change the import line:

```python
# before
from sales_calculations import load_data, total_sales, total_orders, monthly_trend

# after
from sales_calculations import (
    load_data,
    total_sales,
    total_orders,
    monthly_trend,
    sales_by_category,
    sales_by_region,
)
```

Append to the end of the file:

```python
def test_sales_by_category_sorted_descending(sample_df):
    result = sales_by_category(sample_df)

    assert list(result["category"]) == ["Electronics", "Accessories", "Audio"]
    assert list(result["total_amount"]) == [50.00, 15.00, 10.00]


def test_sales_by_region_sorted_descending(sample_df):
    result = sales_by_region(sample_df)

    assert list(result["region"]) == ["North", "South", "East"]
    assert list(result["total_amount"]) == [50.00, 15.00, 10.00]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'sales_by_category'`

- [ ] **Step 3: Implement sales_by_category and sales_by_region**

Append to `sales_calculations.py`:

```python
def sales_by_category(df):
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df):
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Add the category and region charts to app.py**

Modify `app.py`:

```python
import plotly.express as px
import streamlit as st

from sales_calculations import (
    load_data,
    total_sales,
    total_orders,
    monthly_trend,
    sales_by_category,
    sales_by_region,
)

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

df = load_data("data/sales-data.csv")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

trend = monthly_trend(df)
trend_fig = px.line(
    trend,
    x="month",
    y="total_amount",
    title="Monthly Sales Trend",
    labels={"month": "Month", "total_amount": "Sales ($)"},
    markers=True,
)
st.plotly_chart(trend_fig, use_container_width=True)

category_col, region_col = st.columns(2)

category_data = sales_by_category(df)
category_fig = px.bar(
    category_data,
    x="category",
    y="total_amount",
    title="Sales by Category",
    labels={"category": "Category", "total_amount": "Sales ($)"},
    category_orders={"category": list(category_data["category"])},
)
category_col.plotly_chart(category_fig, use_container_width=True)

region_data = sales_by_region(df)
region_fig = px.bar(
    region_data,
    x="region",
    y="total_amount",
    title="Sales by Region",
    labels={"region": "Region", "total_amount": "Sales ($)"},
    category_orders={"region": list(region_data["region"])},
)
region_col.plotly_chart(region_fig, use_container_width=True)
```

- [ ] **Step 6: Verify both charts render correctly**

Run: `streamlit run app.py`
Expected: two bar charts side by side below the trend chart. Category chart's tallest bar is Electronics; both charts show bars in strictly descending order left to right; all 5 categories and all 4 regions appear. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_calculations.py tests/test_sales_calculations.py app.py
git commit -m "TASK-5: Add category and region breakdown charts"
```

---

### Plan Step 6 — Milestone: TASK-6 (Testing and refinement)

**Files:** none expected to change unless verification surfaces an issue.

**Interfaces:** none — this step verifies the whole app built in Plan Steps 1–5 against the PRD's acceptance criteria, it does not add new functions.

- [ ] **Step 1: Run the full test suite**

Run: `pytest tests/test_sales_calculations.py -v`
Expected: PASS (6 tests: `load_data`, `total_sales`, `total_orders`, `monthly_trend`, `sales_by_category`, `sales_by_region`)

- [ ] **Step 2: Run the app and check the terminal for warnings**

Run: `streamlit run app.py`
Expected: no errors or warnings printed in the terminal on startup or while interacting with the charts.

- [ ] **Step 3: Cross-check displayed values against the PRD's Expected Output table**

In the browser, confirm:
- Total Sales ≈ $116,500 (PRD's documented estimate)
- Total Orders = 482
- Top category (tallest bar) = Electronics
- All four regions shown: North, South, East, West

If any value doesn't match, the bug is in the corresponding function in `sales_calculations.py` — fix it there, re-run the relevant pytest test to confirm the fix, then re-run this step.

- [ ] **Step 4: Confirm professional appearance**

Check: chart titles and axis labels are present and legible (already added in Plan Steps 4–5), KPI numbers are comma-formatted, layout doesn't feel cramped at the browser's default width. Stop the server once confirmed.

- [ ] **Step 5: Commit, if Step 3 or 4 required a fix**

```bash
git add sales_calculations.py app.py
git commit -m "TASK-6: Fix <describe the specific issue found>"
```

If no issues were found in Steps 3–4, there is nothing new to commit — `TASK-6` is satisfied by this verification pass over the commits already made in Plan Steps 3–5.

---

### Plan Step 7 — Milestone: TASK-7 (Deployment to Streamlit Community Cloud) — **your manual step**

This step is **not performed as part of this plan**. It's recorded here so the full milestone list is visible, and it's yours to execute after this branch is merged to `main`:

1. Push `feature/sales-dashboard` and open a PR into `main`; merge it once you're satisfied.
2. From `main`, go to [share.streamlit.io](https://share.streamlit.io), sign in, and create a new app pointing at this repository, `main` branch, `app.py` as the entry point.
3. Deploy, then open the generated public URL and confirm the dashboard matches what you verified locally in Plan Step 6.
4. Record the public URL wherever you're tracking stakeholder-facing links (not part of this repo's plan).

The implementation plan ends at Plan Step 6. No further plan steps or agent action follow this one.
