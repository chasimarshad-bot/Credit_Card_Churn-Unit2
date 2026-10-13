# Deployment: Streamlit Community Cloud

Live dashboard: [https://creditcardchurn-unit2-iaagzfaqp5pcffhj3yicmh.streamlit.app/](https://creditcardchurn-unit2-iaagzfaqp5pcffhj3yicmh.streamlit.app/).

Status: deployed. On 12 October 2026 the user supplied a screenshot showing the rendered overview, matching customer counts, charts and filters, then confirmed the dashboard works. Automated HTTP requests alone had returned the Streamlit platform shell; hosted verification is therefore based on the screenshot and user confirmation, alongside the local interaction tests.

## Hosting configuration

- Repository: `chasimarshad-bot/Credit_Card_Churn-Unit2`
- Branch: `main`
- Entry point: `app.py`
- Python: 3.12
- Dependencies: root `requirements.txt` (dashboard runtime only; offline analysis uses `requirements-unit2.txt`)
- Application secrets: none

Generated reports are committed so the dashboard does not train a model at startup. Source updates pushed to the deployed branch are managed by Streamlit Community Cloud; inspect its logs if a later update fails.

## Why Render is not required

Render was an alternative considered before Streamlit Community Cloud deployment. It was never a second requirement. The unused Render configuration and deployment links have been removed so there is one documented hosting route. No Render account or connection is needed.

## Maintenance checks

After a code or dependency update, check all four tabs, change a filter and reset it, inspect a small Platinum-only segment and download the aggregate summary. Model review should show average precision 0.922 for the fixed test set. These checks do not replace a formal accessibility audit.

Official guide: [Streamlit Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
