# JMeter-Testing Workflow Changes

## Summary
These updates were made for the GitHub Actions workflow `JMETER-TESTING`.

## Changes Made
1. Added `checks: write` permission so the test report can be published in GitHub Actions.
2. Added a Python install step because the workflow runs a Python script to convert JMeter results (`.jtl`) to JUnit format (`Junit.xml`).
3. Changed the runner from self-hosted to `windows-latest` so the workflow can run on GitHub-hosted machines.
4. Added JMeter download and install in the script to a fixed path (`C:\JMeter`) because GitHub-hosted runners do not come with JMeter preinstalled.
5. Used the full JMeter executable path explicitly because calling only `jmeter` was not recognized reliably.
6. In the ADO version, Python and JMeter had to already be installed on the agent. In the new version, tools are set up during the workflow run (or can be preconfigured on runners if using self-hosted).
7. Script steps were changed because the runner configuration is different between ADO/self-hosted and GitHub-hosted environments.

## Testing Note
Dummy Python and test files were created using Copilot to validate the Python and JMeter XML conversion flow.

## GitHub Actions YAML Testing Link
https://github.com/ms-pwc/adomg-test/actions/workflows/jmeter-testing.yml