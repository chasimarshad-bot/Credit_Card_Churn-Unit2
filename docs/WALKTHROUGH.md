# Project walkthrough

Use this as a review route, not a script claiming personal experience.

## 1. State the business question

A retention analyst wants to understand recorded customer attrition and explore account activity patterns. The snapshot contains 10,127 customers, including 1,627 marked attrited. The project describes associations and tests a status classifier; it cannot establish future lead time or the benefit of outreach.

## 2. Show the source and ETL

Open `src/data.py`. Explain the validation checks and why the raw file is preserved. Show that customer identifiers, stored classifier outputs and redundant open-to-buy are excluded. Unknown demographics become missing without dropping customers. Show `quality.json` and the cleaned export.

## 3. Explain the statistical evidence

Open notebook 05. Explain mean versus median, spread, conditional probability and Wilson intervals. H1 and H2 compare distributions using Mann-Whitney U; H3 tests product-count independence using chi-square. Explain the effect signs, Holm correction and why significance does not imply causation. These follow previous exploration, so they are exploratory results.

## 4. Explain the classifier

Open notebook 06. Identify the positive class and ten numerical model inputs. Explain why a majority classifier already achieves about 84% accuracy, then why AP, precision and recall are more useful. Model choice uses training CV; threshold choice uses validation; test data assesses those locked decisions. The test records 315 true positives, 198 false positives, 11 false negatives and 1,502 true negatives.

A threshold of 0.25 is a score cut-off, not a calibrated future churn probability. Contact timing is uncertain; removing that feature barely changes validation AP. Other fields still require timing verification.

## 5. Demonstrate the dashboard

Start `python -m streamlit run app.py`. Show each tab, select a product range, inspect the product-rate table, clear the card selection and reset it. Select Platinum to show the small-sample warning. Explain that Model review always uses the fixed test set even when sidebar filters change descriptive views. Demonstrate the aggregate CSV download.

## 6. Explain limitations and next steps

The snapshot has no time window, independent external test or campaign-cost data. Prior Unit 1 exploration limits the independence of the internal holdout. A production study needs dated features, an external/temporal test, calibration, subgroup review, agreed error costs and an outreach experiment.

## 7. Explain the development evidence

Show the GitHub commits, project board and automated checks. Explain which work was imported and which was added for Unit 2. Review the assistance record and add Asim's own learning account after he has run and understood the project.
