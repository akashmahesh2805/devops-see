# Flask Jenkins Pipeline

This repository contains a small Flask service and a declarative Jenkins pipeline. The pipeline creates a Python virtual environment, installs the pinned application dependency, runs the unit test, copies the service to `deployment/`, starts it, and checks its HTTP status and response body.

## Jenkins agent requirements

- Python 3.12 or 3.13 with `venv`
- A POSIX shell and Git
- Network access to install the pinned packages from `requirements.txt`

The Python requirement applies to the agent that runs the Pipeline, not just the Jenkins controller. The Build stage checks the Python version and stops immediately if it is outside the supported range. It bootstraps pip inside its isolated virtual environment, so a system-wide pip installation is not required; the agent needs access to `bootstrap.pypa.io` and PyPI.

## Configure a Jenkins Pipeline job

1. Create a **Pipeline** job in Jenkins.
2. Under **Pipeline**, select **Pipeline script from SCM** and choose **Git**.
3. Set the repository URL to `https://github.com/akashmahesh2805/devops-see.git`, the branch to `*/main`, and the script path to `Jenkinsfile`.
4. Save and select **Build Now**. The Git repository is public, so no checkout credential is required.

The `Test` stage gates `Deploy`, `Run Application`, and `Test Application`; a failed unit test therefore prevents deployment. The success and failure post actions are printed in the Jenkins console output.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v test_app
```
