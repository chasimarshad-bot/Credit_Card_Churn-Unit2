# Streamlit deployment

Status: repository/app prepared; a live host URL has not yet been verified.

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with the GitHub identity that can access the Unit 2 repository.
2. Select **Create app**, then the existing GitHub app option.
3. Repository: `chasimarshad-bot/Credit_Card_Churn-Unit2`.
4. Branch: `main`. Entry point: `app.py`.
5. In Advanced settings choose Python **3.12**. No application secrets are required.
6. Deploy and inspect the dependency/startup logs. The root requirements file includes `requirements-unit2.txt`.
7. Check all four tabs, filters, reset, a Platinum-only segment and aggregate download. Confirm the Model review shows AP 0.922 and the expected test counts.
8. Add the returned live URL to the README and update this status only after successful hosted checks.

Generated reports are committed so the app does not train a model during startup. The app reads the supplied snapshot through the same validation/cleaning functions as the notebooks. It writes no runtime customer records and needs no database.

See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). If build dependencies fail, capture the actual host error and fix it; local interaction tests do not prove a clean Linux/cloud install.

## Render alternative

The root `render.yaml` defines a Python web service using the free compute plan, a pip build, Streamlit bound to the supplied PORT and the Streamlit health endpoint. It has no secrets or database. A service is not created by committing this file.

Install/connect the Render integration to allow deployment from this conversation, or create a Blueprint from this repository in Render. Review the returned service configuration, build logs and live URL. Free-host availability and startup latency are subject to the host's current terms. Do not mark hosting complete based only on the configuration file.

Configuration reference: [Render Blueprint specification](https://render.com/docs/blueprint-spec).
