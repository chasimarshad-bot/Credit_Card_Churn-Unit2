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

## Submission audit follow-up

The submission audit cross-checks the raw digest and cleaned export, recorded split membership, held-out labels and recomputed metrics, saved hypothesis statistics, valid executed notebooks, local documentation links and Git author/committer identity. These checks pass. The strict submission-ready check intentionally remains unsuccessful while live hosting and learner review are unverified.

The audit found damaged punctuation in the README (including negative effect-size signs) and broken figure links in the archived README after it moved into `docs/`. Both were corrected. Validation now rejects text-typed numerical columns with an explicit error rather than failing later during arithmetic; the corrupt-input regression test covers that case. All seven tests continue to pass.

The audit accepts LF/CRLF checkout differences when comparing the original source digest; any other source-content change fails the check. This keeps the same content check usable with both Git checkouts and GitHub source ZIPs.

Dashboard follow-up: transaction frequency, contact rates, classification outcomes and feature reliance now have expandable table alternatives. The dashboard test checks that frequency counts total 10,127, each status share totals 100%, classification outcomes total 2,026 and all ten feature labels are readable without column-name underscores. The model/data outputs are unchanged.

Hosted URL supplied on 12 October 2026: https://creditcardchurn-unit2-iaagzfaqp5pcffhj3yicmh.streamlit.app/. Cookie-aware HTTP requests returned status 200 and the Streamlit platform HTML. The health path also returned platform HTML rather than a definitive app health response; successful Python startup and browser interactions have not been inferred from these responses.

## Hosted verification completed

On 12 October 2026 the user supplied a hosted-dashboard screenshot showing 10,127 customers, 1,627 attrited customers, 16.1% attrition, charts and filters. The user then confirmed that it works. Hosted verification is recorded as complete on that evidence; it is not described as an automated browser test. The unused Render setup was removed because Streamlit Community Cloud already hosts the application. Earlier pending-hosting notes above describe the state before this confirmation.

Personal learner review remains unverified. No personal learning experience or assessment submission has been invented.

## Reliability review and follow-up

Twelve tests pass after adding report consistency checks and graceful handling of unavailable model/source evidence. The model-report failure test verifies that portfolio metrics remain usable. Table rates use explicit percentage units and readable headings. Compilation and dependency checks also pass. Model training, split assignments and numerical results are unchanged.

The independent technical review is in `TECHNICAL_REVIEW.md`. Its publication judgement is scoped to the educational dashboard; formal load/security/accessibility audits and suitability for banking decisions are not claimed. The latest update needs the normal post-deployment hosted smoke check; the earlier screenshot/user confirmation remains the record for initial hosted operation.
