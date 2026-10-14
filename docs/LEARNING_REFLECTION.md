# Development reflection and learner review

This document contains the technical development account and Asim's supplied personal reflection. The optional [technical quality review](TECHNICAL_REVIEW.md) separately records implementation checks.

## Technical changes evidenced in this implementation

The original analysis used sequential notebook steps. Unit 2 moves validation, cleaning, hypothesis tests and modelling into reusable modules. This reduces transformation duplication and gives the dashboard the same source of cleaned data as the notebooks.

The source contains stored classifier outputs. A feature whitelist excludes them and the original/derived target from model inputs. Model selection uses training cross-validation, threshold selection uses validation, and the internal test is scored after those decisions. Prior Unit 1 inspection of the full dataset limits the independence of that test.

Class imbalance makes accuracy misleading: the majority baseline is about 84% accurate while detecting no attrited customers. AP, precision, recall and error counts give a more useful evaluation. A validation threshold expresses a recall/precision trade-off; without business costs it cannot demonstrate financial benefit.

A scatter plot can hide dense observations. Hexbin and density views reveal where customers concentrate, while labels distinguish counts from probabilities. Wilson intervals and small-sample messages discourage overinterpreting narrow segments.

Streamlit interaction testing exposed a filter-reset defect. Clearing session state did not restore widget selections; explicit widget keys and a reset callback corrected it. The regression test now checks the restored full-population count.

A fresh installation exposed PyArrow 26 requiring NumPy 2 at runtime despite successful dependency resolution. Pinning PyArrow 25.0.1 restored compatibility; the dashboard regression test passed in the fresh environment.

A separate lean dependency file removes the need to install optional legacy profiling helpers for the dashboard. UTF-8 without a BOM is used for TOML configuration because the installed parser rejected a BOM.

## Asim's personal reflection

Provided by Asim through the project mentor on 12 October 2026.

My main takeaway from this project was that customers who made fewer transactions were more likely to leave. It was interesting to see this pattern in the data, although I understand that it doesn't necessarily mean low activity was the reason they left.

We compared Logistic Regression and Random Forest to see which model performed better. Logistic Regression was a good starting point because it's simple and easier to understand, whereas Random Forest can identify more complex patterns. Random Forest gave better results based on the metric we used, which is why we selected it. However, I also learned that no model is perfect, and some predictions can still be wrong.

One thing I learned was how to use the dashboard to explore the data through different filters and charts. It helped me understand the results better rather than just looking at numbers.

I also realised how important it is to check the results properly. Initially, understanding the model predictions and the difference between the two models was a bit confusing, but going through the results and explanations helped me make more sense of them.

AI and mentor guidance helped me understand the technical parts of the project, especially the model comparison and how to interpret the results. However, I know it's important not to rely entirely on AI, so I focused on understanding the findings and checking them against the project results.

If I were to improve the project, I would use more recent customer data and include information about when customers actually left. I think this would help us understand churn better and potentially identify customers at risk before they leave.

## Walkthrough confirmation

The reflection has been received. The user confirmed on 14 October 2026 that Asim completed his independent walkthrough. Use the [walkthrough guide](WALKTHROUGH.md) to demonstrate filtering, explain the training/validation/test partitions and threshold choice, and describe the limits of predictions from a historical snapshot.
