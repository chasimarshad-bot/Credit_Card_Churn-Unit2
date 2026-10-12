# Submission checklist

## Submission links

- Source: https://github.com/chasimarshad-bot/Credit_Card_Churn-Unit2
- Commit history: https://github.com/chasimarshad-bot/Credit_Card_Churn-Unit2/commits/main/
- Project board: https://github.com/users/chasimarshad-bot/projects/3
- Release candidates: https://github.com/chasimarshad-bot/Credit_Card_Churn-Unit2/releases
- Live dashboard: pending deployment; use the actual returned URL, never a proposed hostname.

## Technical evidence

- [x] Clear business purpose and audience.
- [x] Source dataset and imported Unit 1 work credited.
- [x] Functional ETL with raw/output separation and automated integrity checks.
- [x] Explained and applied statistics/probability.
- [x] Three exploratory hypotheses, corrected tests and effect sizes.
- [x] Justified supervised model, baseline, separate partitions and error analysis.
- [x] Two executed Unit 2 notebooks with saved outputs.
- [x] Interactive dashboard with multiple plot types, filtering and aggregate export.
- [x] Limitations, technical reflection, assistance record and criterion map.
- [x] Genuine commits published under the project account.
- [ ] Hosted dashboard deployment and browser/accessibility review.
- [ ] Asim's personal learning/AI reflection and independent project walkthrough.
- [ ] Confirm the official deadline and submission fields in the LMS.
- [ ] Submit the source and live dashboard links using Asim's registered email.

## Final local check

Run from the repository root with Python 3.12:

```powershell
python -m pip install -r requirements.txt
python -m pip check
python -m unittest discover -s tests -v
python scripts/audit_submission.py
python -m streamlit run app.py
```

The audit verifies raw/export consistency, splits and metrics, saved hypotheses, notebook execution, documentation links and Git attribution. It lists the two evidence gaps rather than silently treating them as complete. `--require-submission-ready` returns a failing exit status until the tracked hosting and learner review status is complete.

Update `submission_status.json` only after the matching evidence exists. Add the verified live URL to the README and deployment guide. Replace the personal reflection prompts with Asim's actual experience; review assistance credits and the assessment form together.

## Commit history and release copies

The initial commit imports the existing Unit 1 snapshot and credits its sources. Subsequent commits contain the Unit 2 modules, executed analysis, dashboard, documentation and fixes. They have their real creation dates; no earlier development timeline has been fabricated. Full original Unit 1 history remains in its linked source repositories.

A release candidate contains a source ZIP and a Git bundle. The ZIP is convenient for review; **GitHub's source ZIP alone does not contain commit history**. Use the `.bundle` to keep the full Unit 2 history offline:

```powershell
git bundle verify Credit_Card_Churn-Unit2-v1.0.0-rc1.bundle
git clone Credit_Card_Churn-Unit2-v1.0.0-rc1.bundle Credit_Card_Churn-Unit2-review
```

The release is a candidate until hosting and learner review are complete. No assessment submission has been made on Asim's behalf.
