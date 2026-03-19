# Mobile Quickstart

Commands below assume you run them from the repo root.

1. Install dependencies: `python -m pip install -r Mobile/requirements-mobile.txt`
2. Create the app: `briefcase create android` or `briefcase create iOS`
3. Build the app: `briefcase build android` or `briefcase build iOS`
4. Package the app: `briefcase package android --adhoc-sign` or `briefcase package iOS --adhoc-sign`
5. Enter your server URL and API token inside the mobile app UI.
