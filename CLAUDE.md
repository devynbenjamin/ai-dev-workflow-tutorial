# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a student project built while working through an AI-assisted development workflow tutorial (see `README.md`). The deliverable is a single-page Streamlit sales dashboard for a fictional retailer, ShopSmart, built from `prd/ecommerce-analytics.md`. The tutorial content itself (`pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`) is instructional material, not part of the app.

The build follows a traceable, milestone-driven workflow: `prd/ecommerce-analytics.md` (requirements) → `TASKS.md` (milestone board, IDs like `TASK-1`) → design/plan docs under `docs/superpowers/` → code, committed with the milestone ID in each commit message. `git log` is the audit trail from requirement to shipped code — check `TASKS.md` and recent commits before starting new work to see what milestone is active and what's already done.

## Commands

Activate the virtual environment first (created at `venv/`, not committed):

```bash
source venv/bin/activate
```

Run the app:

```bash
streamlit run app.py
```

Run the full test suite:

```bash
pytest tests/test_sales_calculations.py -v
```

Run a single test:

```bash
pytest tests/test_sales_calculations.py::test_total_sales_sums_all_transactions -v
```

`pytest.ini` sets `pythonpath = .`, which is required for bare `pytest` invocations to resolve the top-level `sales_calculations` module — without it, pytest's default import mode only puts the test file's own directory on `sys.path`.

Dependencies are exact-pinned in `requirements.txt` (`pandas`, `plotly`, `pytest`, `streamlit`). If you add a dependency, install it into `venv/` then regenerate pins with `pip freeze | grep -iE '^(streamlit|pandas|plotly|pytest)==' > requirements.txt` rather than hand-editing version numbers.

## Architecture

Two files carry all the application logic:

- **`sales_calculations.py`** — pure data functions only (`load_data`, `total_sales`, `total_orders`, `monthly_trend`, `sales_by_category`, `sales_by_region`). No Streamlit or Plotly imports. This is what makes the module unit-testable with pytest using hand-crafted in-memory DataFrames, independent of the real CSV or any UI framework.
- **`app.py`** — the Streamlit page. Loads the DataFrame once via `load_data("data/sales-data.csv")`, then renders KPI metrics and Plotly Express charts built directly from the aggregation functions above.

Keep that separation when extending the dashboard: new calculations belong in `sales_calculations.py` with matching tests in `tests/test_sales_calculations.py`; `app.py` should only call those functions and wire up Streamlit/Plotly rendering, never contain aggregation logic itself.

`data/sales-data.csv` is treated as a known, well-formed file — there's no schema/type validation beyond pandas' own CSV parsing (482 transaction records, columns: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`). Tests use hand-crafted fixtures or temp CSVs, never the real data file.

## Conventions specific to this project

- Dashboard title is exactly `"ShopSmart Sales Dashboard"` — the PRD mockup's "SHOPMART" is a typo against the company name used throughout the PRD.
- Trend chart uses monthly granularity, not daily.
- Bar charts are vertical, sorted descending by sales value (both in the aggregation function's sort and via Plotly's `category_orders`, since Plotly would otherwise re-sort alphabetically).
- No code comments beyond what's already established in the codebase — keep it simple and readable.
- Streamlit is pinned to 1.64.0, which deprecates `use_container_width` on chart calls in favor of `width="stretch"`/`width="content"` — use the `width=` form, not `use_container_width`.

## Planning artifacts

`docs/superpowers/specs/` and `docs/superpowers/plans/` hold the design spec and implementation plan for the dashboard (written using the Superpowers skills referenced in `README.md`). The plan's own step numbering ("Plan Step 1"–"Plan Step 7") is deliberately distinct from the `TASKS.md` milestone IDs ("TASK-1"–"TASK-7") it maps to one-to-one — don't conflate the two in commits or notes.

Deployment (`TASK-7`, PRD milestone M7, Streamlit Community Cloud) is a manual step performed by the student after merging to `main` — it is not something Claude should attempt to execute.

## Lessons

Distilled from the `Notes:` lines in `TASKS.md` — read those for full context.

- Read a file before overwriting it, even one that looks boilerplate. Blindly writing a fresh `.gitignore` clobbered a 231-line curated version (`TASK-1`).
- An acceptance criterion that looks unimplemented may be intentionally out of scope — check the implementation plan before adding validation/error handling to satisfy it. `sales_calculations.py` deliberately skips CSV schema/type validation beyond pandas' own parsing (`TASK-2`).
- A quick headless `streamlit run` check can exit before the script body fully executes, producing a clean-looking log that's a false negative. To actually verify "no warnings on startup," hit the running app (e.g. `curl`) or exercise it interactively before trusting the terminal output (`TASK-6`).
