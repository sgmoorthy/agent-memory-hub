# Publishing Guide

This guide explains how to publish the `agent-memory-hub` package to PyPI.

## Prerequisites

1.  **PyPI Account**: You must have an account on [PyPI](https://pypi.org/).
2.  **GitHub Secrets**: You need to configure a secret in your GitHub repository to allow the CI workflow to authenticate with PyPI.

## Step 1: Generate an API Token

1.  Log in to your [PyPI account](https://pypi.org/manage/account/).
2.  Go to **Account Settings** -> **API Tokens**.
3.  Click **Add API Token**.
4.  **Token Name**: `agent-memory-hub-github-action` (or similar).
5.  **Scope**: Select "Entire account (all projects)" for the first publish (since the project doesn't exist yet). _After the first publish, you can scope it to just this project._
6.  Click **Add Token**.
7.  **Copy the token immediately**. It will start with `pypi-`.

## Step 2: Configure GitHub Secrets

1.  Go to your GitHub repository.
2.  Click **Settings** -> **Secrets and variables** -> **Actions**.
3.  Click **New repository secret**.
4.  **Name**: `PYPI_API_TOKEN`
5.  **Secret**: Paste the token you copied from PyPI.
6.  Click **Add secret**.

## Step 3: Trigger a Release

The publishing process is automated. To publish a new version:

1.  Update the `version` in `pyproject.toml` (e.g., to `0.1.1`).
2.  Commit and push changes.
3.  Go to the **Releases** section in your GitHub repository.
4.  Draft a new release.
    - **Tag version**: `v0.1.1`
    - **Title**: `Release v0.1.1`
5.  Click **Publish release**.

The `.github/workflows/publish.yml` workflow will automatically run, build the package, and upload it to PyPI.
