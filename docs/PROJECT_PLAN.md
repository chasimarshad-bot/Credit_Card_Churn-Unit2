# Unit 2 project plan

Audience: a bank retention analyst. Goal: explore recorded attrition and evaluate whether account activity distinguishes the recorded outcomes. The dataset cannot test future lead time or campaign effectiveness.

GitHub board: https://github.com/users/chasimarshad-bot/projects/3

## Task board

This is the actual implementation record, not a reconstructed daily history. The Unit 1 files were imported as existing work.

| Task | Acceptance evidence | Status |
|---|---|---|
| Define audience and four business requirements | README and notebook introductions | Done |
| Retain and credit Unit 1 material | Original notebooks and archived README | Done |
| Validate raw source and record its digest | `src/data.py`, `quality.json` | Done |
| Separate ETL into reusable functions | Validation, cleaning and export functions | Done |
| Explain core statistics and probability | Notebook 05 | Done |
| Test three exploratory hypotheses | Corrected p-values, effect sizes, expected counts | Done |
| Improve dense visual exploration | Hexbin and interactive density views | Done |
| Compare classification methods | Logistic regression and random forest training CV | Done |
| Select operating threshold on validation | Threshold table and stated precision constraint | Done |
| Evaluate locked model on internal test | Confusion matrix, AP/ROC curves and baseline | Done |
| Review contact timing sensitivity | Validation AP with/without contacts | Done |
| Build interactive dashboard | Four tabs, segment filters and aggregate export | Done |
| Test bad input and dashboard interactions | Thirteen passing automated tests | Done |
| Execute and save both Unit 2 notebooks | All code cells have execution counts; no error outputs | Done |
| Document limits, setup and assistance | README and supporting documentation | Done |
| Publish separate repository | GitHub repository published under chasimarshad-bot | Done |
| Deploy and check hosted Streamlit app | Streamlit Community Cloud URL, user screenshot and confirmation | Done |
| Review personal learning and submission | Asim's own reflection and walkthrough | Reflection received; walkthrough pending |

## MoSCoW

**Must:** valid ETL, statistical explanation/application, hypothesis validation, justified ML, interactive tool, two plot types, evaluation, structured plan, attribution, runnable documentation and hosted Streamlit delivery.

**Should:** uncertainty intervals, model baseline, split audit, threshold trade-offs, modular transformations and automated integrity checks. Implemented.

**Could:** external temporal validation, subgroup performance analysis, score calibration and an intervention-cost simulator. Deferred until the required data is available.

**Won't in this version:** live bank integration, real customer eligibility decisions, claims of causal retention benefit or future churn probability.

## Delivery and schedule

The supplied meeting notes repeatedly state 14 October 2026 at 17:00, but also contain one mention of 15 October. Treat 14 October as the conservative planning date and confirm the official deadline in the LMS. No submission has been made by this implementation.

Deployment is complete, supported by the user screenshot and confirmation. Asim's personal reflection has been received. Confirmation of his independent walkthrough remains outstanding before submission. The supplied handbook is the assessment reference; the meeting notes and templates provide supporting guidance.
