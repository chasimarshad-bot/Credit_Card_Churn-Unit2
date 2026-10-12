# Development reflection and learner review

The completed [independent technical review](TECHNICAL_REVIEW.md) assesses the implementation for Asim. It is separate from his personal reflection.

## Technical changes evidenced in this implementation

The original analysis used sequential notebook steps. Unit 2 moves validation, cleaning, hypothesis tests and modelling into reusable modules. This reduces transformation duplication and gives the dashboard the same source of cleaned data as the notebooks.

The source contains stored classifier outputs. A feature whitelist excludes them and the original/derived target from model inputs. Model selection uses training cross-validation, threshold selection uses validation, and the internal test is scored after those decisions. Prior Unit 1 inspection of the full dataset limits the independence of that test.

Class imbalance makes accuracy misleading: the majority baseline is about 84% accurate while detecting no attrited customers. AP, precision, recall and error counts give a more useful evaluation. A validation threshold expresses a recall/precision trade-off; without business costs it cannot demonstrate financial benefit.

A scatter plot can hide dense observations. Hexbin and density views reveal where customers concentrate, while labels distinguish counts from probabilities. Wilson intervals and small-sample messages discourage overinterpreting narrow segments.

Streamlit interaction testing exposed a filter-reset defect. Clearing session state did not restore widget selections; explicit widget keys and a reset callback corrected it. The regression test now checks the restored full-population count.

A fresh installation exposed PyArrow 26 requiring NumPy 2 at runtime despite successful dependency resolution. Pinning PyArrow 25.0.1 restored compatibility; the dashboard regression test passed in the fresh environment.

A separate lean dependency file removes the need to install optional legacy profiling helpers for the dashboard. UTF-8 without a BOM is used for TOML configuration because the installed parser rejected a BOM.

## Asim's personal reflection - complete after running the project

The account above describes observed implementation changes; it does not represent Asim's personal experience. Add concise answers in your own words:

1. Which method or tool did you learn, and what can you now explain or do yourself?
2. Which actual problem did you encounter while running/reviewing this project? How did you resolve it?
3. Which result changed your understanding of the business problem?
4. Which assistance did you accept, modify or reject, and how did you check it?
5. What would you change with dated data or more time, and why?

Before submission, demonstrate the dashboard, explain the split/threshold protocol, distinguish association from causation and describe why this model is not a proven future churn forecast. Do not replace these prompts with invented experiences.
