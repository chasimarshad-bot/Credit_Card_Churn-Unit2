# Independent technical review for Muhammad Asim

Reviewer: OpenAI Codex, with Sanif coordinating the work. Date: 12 October 2026.

This is the reviewer's assessment of the implementation and test evidence. It is not a statement of Asim's personal experience or unaided authorship.

## Overall judgement

The project is a coherent, reproducible educational analysis with a deployed dashboard. Its main strengths are explicit leakage exclusions, a justified comparison of two classifiers, transparent uncertainty and an appropriately limited interpretation of snapshot data. The reviewed code is suitable for publication as an educational analytics application within that scope. It has not been qualified as a banking decision system or future churn forecasting service.

## Analysis and modelling

The ETL preserves the original snapshot and separates validation from transformation. It rejects duplicate customer IDs, ambiguous labels, nonnumeric numerical columns and invalid value domains. Converting Unknown demographics to missing while preserving rows avoids inventing demographic facts. Failure to detect a missingness association does not establish random missingness, and the documentation now makes that limit explicit.

The stored Naive Bayes columns would leak the outcome and are excluded, together with identifiers and target fields. Logistic regression and random forest are compared using training-only stratified cross-validation. Random forest is selected by mean average precision. The operating threshold is selected on validation rather than test data; the majority classifier shows why accuracy alone would mislead.

The internal test detects 315 of 326 attrited customers, with 198 false alarms and 11 misses. Average precision is approximately 0.922, recall 96.6% and precision 61.4%. These numbers are internally consistent with the saved predictions and split assignments. They demonstrate retrospective classification within this known dataset. They do not establish advance warning, retention benefit or a financially optimal outreach policy.

The three exploratory hypotheses include effect sizes and Holm adjustment. Distributional comparisons are correctly distinguished from causal conclusions. Prior full-snapshot Unit 1 exploration prevents treating the internal holdout as an independent external study. Removing contact count has little effect on validation AP, but measurement timing still needs verification across all activity fields.

## Dashboard and operational reliability

The four-tab dashboard has a clear audience, labelled charts, reversible filters, an explicit missing-data choice and a small-sample warning. Tables provide alternatives to colour and hover. Aggregate downloads avoid introducing an individual-record export. Product and contact rates now use explicit percentage units and readable headings.

Review identified a failure path where unavailable or inconsistent model evidence could interrupt the dashboard. Saved report validation now checks metrics, confusion counts, test population and feature importance. When model evidence is unavailable, descriptive views remain available and Model review shows a clear message. Invalid source data produces a clear unavailable-data message rather than an unhandled application exception. Detailed diagnostic errors stay in host logs.

The app performs no model training at startup, needs no application secrets and uses a single documented Streamlit Community Cloud host. The unused Render configuration was removed. The user supplied a screenshot of the deployed overview and confirmed operation before the latest reliability update. The latest update passed local interaction tests; a separate hosted browser regression check after the update is recommended.

## Verification evidence

- Both Unit 2 notebooks have valid structure, saved execution counts and no error outputs.
- The submission audit checks source/export consistency, hypothesis results, split membership, test labels/predictions, metrics, local documentation links and Git attribution.
- Twelve automated tests pass, covering corrupt input, split isolation, statistical guardrails, saved report consistency, filter/reset behaviour, readable tables and graceful failures.
- Dependency checking and Python compilation pass in the Python 3.12 environment.
- Hosted rendering/operation is supported by the user screenshot and confirmation; this is distinguished from automated browser testing.

## Remaining limits and priorities

For the current public educational application, maintain the pinned environment, inspect Streamlit logs after updates and repeat the documented smoke checks. There has been no formal load test, security audit or full assistive-technology accessibility audit; this review does not imply those were completed.

For a real retention application, obtain dated features before a defined outcome horizon, independent temporal/external data, calibration and subgroup error evidence. Agree error/outreach costs and measure intervention benefit experimentally before using scores for customer decisions.

For the assessment, the implementation and independent review provide technical evidence. Asim's personal reflection has since been received. Independent walkthrough confirmation and LMS submission remain outstanding. This review cannot certify participation or guarantee a grade.

Follow-up: the [13 October readiness review](READINESS_REVIEW.md) records subsequent fixes, thirteen tests and dependency auditing.
