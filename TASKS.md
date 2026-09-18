# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard, based on `prd/ecommerce-analytics.md`.

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the commit message

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard so it's publicly accessible via a shareable URL (corresponds to PRD milestone M7, NFR-5).

- [ ] App deployed to Streamlit Community Cloud
- [ ] Public URL loads the dashboard correctly with no errors
- [ ] Deployed version matches the locally verified version

Commit:

## In Progress

## Done

### TASK-6: Testing and refinement
Verify the dashboard meets all acceptance criteria and polish for presentation (corresponds to PRD milestone M6).

- [x] All values match expected calculations from the CSV
- [x] Dashboard runs without errors or warnings and loads within 5 seconds
- [x] Layout and labels are clear and suitable for an executive presentation

Commit: 731b962
Notes: Claude's first verification pass wrongly reported "no warnings" — a headless run exited before the app script fully executed, so the clean-looking log was a false negative. The `use_container_width` deprecation warnings (Streamlit 1.64.0 replacing it with `width=`) only surfaced once the app was run interactively for the user to test. Fixed by switching all three `st.plotly_chart` calls to `width="stretch"`; a fresh run then showed a clean terminal and pytest still passed 6/6.

### TASK-5: Category and region breakdowns
Add the category and region bar charts (corresponds to PRD milestone M5, FR-3, FR-4).

- [x] Category bar chart shows all 5 categories, sorted by sales value
- [x] Region bar chart shows all 4 regions, sorted by sales value
- [x] Both charts have interactive tooltips with exact values

Commit: 5300b3c
Notes: Clean.

### TASK-4: Sales trend chart
Add the sales-over-time line chart (corresponds to PRD milestone M4, FR-2).

- [x] Line chart shows sales over time with correct data
- [x] Interactive tooltips show exact values
- [x] Chart renders within 2 seconds of data load

Commit: ce97866
Notes: Clean.

### TASK-3: KPI cards implementation
Display the Total Sales and Total Orders KPIs (corresponds to PRD milestone M3, FR-1).

- [x] Total Sales displayed as currency (~$116,500, formatted as $X,XXX,XXX)
- [x] Total Orders displayed as a formatted count (482)
- [x] KPIs are visually prominent on the dashboard

Commit: bcdba3a
Notes: Clean.

### TASK-2: Data loading and basic structure
Load `sales-data.csv` and validate its structure (corresponds to PRD milestone M2, FR-5).

- [x] CSV loads into a Pandas DataFrame with correct column types (date, numeric, categorical)
- [x] All 482 transaction records load without errors
- [ ] Basic data validation (e.g. no missing required columns) is in place

Commit: d8b2c85
Notes: The implementation plan (docs/superpowers/plans/2026-09-14-sales-dashboard.md) deliberately scopes `sales_calculations.py` to no schema/type validation beyond pandas' own CSV parsing, treating the CSV as a known, well-formed file — so the third criterion is intentionally not implemented, not an oversight. Also added `pytest.ini` (`pythonpath = .`) so bare `pytest` resolves the top-level module; without it, pytest's default import mode only puts the test file's own directory on `sys.path`, not the project root.

### TASK-1: Environment setup and project initialization
Set up the Python project structure and dependencies for the dashboard (corresponds to PRD milestone M1).

- [x] Project structure created (e.g. `app.py`, `data/`, `requirements.txt`)
- [x] Dependencies (Streamlit, Plotly, Pandas) install cleanly
- [x] `streamlit run app.py` launches a blank/placeholder app without errors

Commit: 1d8f749
Notes: Claude initially overwrote the existing .gitignore (231 lines of curated patterns) with a 3-line file instead of reading it first — caught before committing and reverted; the original already covered venv/, so no .gitignore change was needed for this task.
