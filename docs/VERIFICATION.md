# Verification record

12 October 2026, local Python 3.12.8 environment.

- `python run_analysis.py`: completed from raw CSV, 10,127 rows and 1,627 attrited customers. Selected random forest using training CV.
- Notebook 05: executed all cells, no error outputs; statistical tables, corrected tests, product intervals and hexbin figure saved.
- Notebook 06: executed all cells, no error outputs; CV comparison, threshold, baseline, test diagnostics, bootstrap and contact sensitivity saved.
- `python -m unittest discover -s tests -v`: seven tests passed. Includes invalid inputs, exclusions, missingness preservation, disjoint stratified splits, Wilson edges, Holm adjustment, threshold constraint and dashboard interactions.
- `python -m compileall -q src app.py run_analysis.py`: passed.
- Dashboard AppTest: initial rendering, empty segment, reset to 10,127 rows, demographic-missing exclusion and 20-customer Platinum segment passed without app exceptions.

A separate fresh Python 3.12.8 virtual environment installed the project requirements. The first dashboard run exposed PyArrow 26 requiring NumPy 2 at runtime; pinning PyArrow 25.0.1 resolved it. After that correction, pip check, all seven tests and compilation passed in the fresh environment.

The local Streamlit HTTP health endpoint also returned `ok`. The generated hexbin figure was visually inspected for labels, scale and readability.

Testing found and resolved a TOML BOM parsing issue, a filter-reset defect and the PyArrow/NumPy conflict. Tests are automated application checks, not a screenshot review or a formal accessibility audit.

Still to verify: clean Linux/cloud installation, hosted URL and browser layout/accessibility. Notebook runtime emitted a Windows event-loop fallback warning; execution completed successfully. No claim of a clean independent environment install is made.
