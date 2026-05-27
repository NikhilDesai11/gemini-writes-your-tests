# gemini-writes-your-tests

`gemini-writes-your-tests` is a Python project that brings AI into a practical CI workflow. It uses GitHub Actions and the Gemini API to run tests, review pull requests, label risk, and generate tests when coverage drops.

## 🚀 Overview

This project shows how to move beyond basic CI and build smarter automation around code quality. It starts with a simple pytest pipeline, then adds AI-powered pull request reviews, severity-based labeling, and automated test generation for changed Python files.

## ✨ Features

- ✅ Run `pytest` automatically on pushes and pull requests
- 📦 Build and upload Python package artifacts in CI
- 🤖 Review pull requests with Gemini using code diffs
- 💬 Post AI review comments directly on pull requests
- 🏷️ Apply severity labels automatically: critical, warning, or looks-good
- 🧪 Generate pytest tests for changed Python files with Gemini
- 📉 Skip test generation when coverage is already above threshold
- 🔁 Commit generated tests back to the pull request branch

## 🛠️ Tech Stack

| Layer | Tooling |
|---|---|
| Language | Python 3.11 |
| Testing | pytest, pytest-cov |
| CI/CD | GitHub Actions |
| AI | Google Gemini API via `google-genai` |
| Packaging | `build` |
| Parsing | Python `ast` |

## ⚙️ Setup

### Prerequisites

- Python 3.11 or newer
- Git
- GitHub account
- Gemini API key from Google AI Studio

### Install

```bash
git clone https://github.com/NikhilDesai11/gemini-writes-your-tests.git
cd gemini-writes-your-tests

python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Authenticates requests to the Gemini API |

For local runs:

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

For GitHub Actions, add `GEMINI_API_KEY` under:

**Repository Settings → Secrets and variables → Actions**

## 🧪 Run Locally

Run tests:

```bash
pytest -v
```

Run the AI review script on a diff file:

```bash
python scripts/ai_review.py scripts/sample_diff.txt
```

Run the test generator on one or more Python files:

```bash
python scripts/generate_tests.py app.py
```

Run the coverage check with an 80% threshold:

```bash
python scripts/check_coverage.py 80
```

Build the package:

```bash
python -m build
```

## 📜 Scripts

| Script | Purpose |
|---|---|
| `scripts/ai_review.py` | Sends a pull request diff to Gemini and returns a structured review |
| `scripts/generate_tests.py` | Extracts function definitions from changed files and generates pytest tests |
| `scripts/check_coverage.py` | Measures test coverage and decides whether test generation is needed |
| `scripts/sample_diff.txt` | Sample diff used for local AI review testing |

## 🤖 API / Architecture

### 1. CI pipeline

The base CI workflow runs on pushes and pull requests to `main`.

Flow:

```text
checkout -> setup Python -> install dependencies -> pytest -> build package -> upload artifact
```

### 2. AI pull request review

The PR review workflow runs on pull requests to `main`.

Flow:

```text
pull request opened/updated
-> get PR diff
-> run ai_review.py
-> post Gemini review comment
-> extract severity
-> apply GitHub label
```

### 3. AI test generation

The test generation workflow runs on pull requests when Python files change.

Flow:

```text
pull request opened/updated
-> check coverage
-> if coverage < threshold, find changed Python files
-> run generate_tests.py
-> write tests/test_generated.py
-> commit generated tests back to PR branch
```

### 🏷️ Severity labels

| Severity | Label |
|---|---|
| CRITICAL | `ai-review: critical` |
| WARNING | `ai-review: warning` |
| GOOD | `ai-review: looks-good` |

## 📂 Folder Structure

```text
gemini-writes-your-tests/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── pr-review.yml
│       └── test-gen.yml
├── scripts/
│   ├── ai_review.py
│   ├── check_coverage.py
│   ├── generate_tests.py
│   └── sample_diff.txt
├── tests/
│   ├── test_app.py
│   └── test_generated.py
├── app.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🚢 Deployment

This project is packaged in CI using:

```bash
python -m build
```

On successful workflow runs, GitHub Actions uploads the contents of `dist/` as a downloadable artifact named `python-package`.

The artifact includes:

- A `.whl` file for installation
- A `.tar.gz` source archive

## 🤝 Contributing

1. Fork the repository
2. Create a branch for your change
3. Make your updates
4. Open a pull request
5. Let the workflows run

If your pull request changes Python code, the repository can automatically review it, label it, and generate tests where needed.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.