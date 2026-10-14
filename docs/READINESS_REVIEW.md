# Readiness review - 13 October 2026

## Outcome

Suitable for publication as an educational snapshot dashboard, subject to a hosted smoke check after this update. This is not a production customer-decision system or a guarantee of assessment marks. Personal reflection is received; independent learner walkthrough confirmation and LMS submission remain outstanding.

## Findings corrected

- Product/contact conclusions previously sounded specific to any filtered segment. They now explicitly refer to the full snapshot and explain that filtered segments can differ.
- Saved evidence validation now checks that displayed precision/recall agree with confusion counts. Baseline metrics reject booleans, strings and non-finite values. Regression coverage exercises these cases.
- Streamlit upgraded from 1.40.2 to 1.54.0, addressing the Windows-specific request-handling advisory [GHSA-7p48-42j8-8846](https://github.com/streamlit/streamlit/security/advisories/GHSA-7p48-42j8-8846). Pillow is pinned to 12.3.0 following dependency scanning.
- Deprecated chart/table sizing arguments replaced with the supported width option.
- Hosted runtime is separated from offline model/notebook tools. The dashboard reads saved evidence and does not need scikit-learn, matplotlib or notebook execution packages.
- Stale personal-reflection and test-count statements corrected. Historical verification entries retain their original counts and dates.

## Security and reproducibility scope

`python -m pip_audit -r requirements.txt --format json` found no known vulnerabilities in the resolved dashboard requirements on 13 October 2026. The [machine-readable report](RUNTIME_DEPENDENCY_AUDIT.json) records the resolved versions. This is a point-in-time advisory scan, not penetration testing or a guarantee against unknown vulnerabilities.

The offline analysis retains scikit-learn 1.3.1 to reproduce the existing executed notebooks and numerical evidence. Its known advisory PYSEC-2024-110 concerns TfidfVectorizer, which this numerical project does not use. This package is excluded from hosted requirements. Do not describe the full offline environment as free of known advisories; upgrading it should include rerunning and reviewing all generated analysis evidence. Local pip was upgraded to 26.2.1 as part of the review.

The public app offers no uploads, user-supplied file paths, executable queries, stored user accounts or individual-record downloads. It uses the supplied historical dataset and exports aggregate segment summaries. Dataset redistribution terms, formal accessibility auditing, load testing and live monitoring remain limitations. No sensitive bank data should be added to this public repository.

## Assessment evidence

The criterion map links statistical explanation/application, three exploratory hypotheses, modular ETL, two-model training comparison, executed notebooks, interactive visualisation, limitations, planning and genuine personal reflection. These strengthen reviewability; only the assessor can determine the grade. No distinction criteria beyond the supplied requirements have been assumed.

## Hosted smoke check

After the updated branch rebuilds, open all four tabs; change and reset filters; select Platinum for the small-sample warning; download the aggregate summary; check the fixed model review still shows AP 0.922. The previous screenshot confirms the earlier hosted version, not this dependency update. Use the host logs if rebuilding fails.

A fresh Windows Python 3.12 runtime-only environment installed root requirements successfully, passed all three dashboard interaction/failure-path tests and passed pip check on 13 October 2026. It contains no scikit-learn or notebook execution tools. Linux hosted rebuild and browser smoke checks remain unverified for this update.

## Hosted browser verification - 14 October 2026

The app was sleeping from inactivity. Its public wake-up button was used and startup completed. Playwright with headless Microsoft Edge then checked the actual hosted Streamlit iframe: all four tabs, the 10,127-customer overview, downloadable aggregate CSV totals, empty selections, Platinum-only 20-customer warning, reset, missing-demographic exclusion and fixed model AP 0.922 under filtering. All checks passed. The [browser audit](HOSTED_BROWSER_AUDIT.json) records the checks; this supersedes the earlier pending post-update smoke check. This browser verification is not evidence of Asim's independent walkthrough or LMS submission.

Streamlit may sleep again after inactivity. If the assessor sees the sleep screen, select "Yes, get this app back up!" and allow startup to finish.
