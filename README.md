![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/KAHLYM/market-prediction/Angular%20Tests/main?label=Angular%20Tests&logo=Angular&style=for-the-badge)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/KAHLYM/market-prediction/Lint/main?label=Linter&style=for-the-badge)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/KAHLYM/market-prediction/Lint/main?label=Linter&style=for-the-badge)
![GitHub Workflow Status (branch)](https://img.shields.io/endpoint?url=https%3A%2F&2Fraw.githubusercontent.com/KAHLYM/market-prediction/main/web-app/functions/get_reddit_submissions/coverage.json&style=for-the-badge)

# Market Prediction

## Languages, Libraries & Frameworks

The frontend is built with [Angular](https://angular.io/) and makes use of [Sass](https://sass-lang.com/).

The backend is built with [Firebase](https://firebase.google.com/).

## Automation

### Main

When a pull request is raised against `main` the following automation executes:
* Angular Build and Test
* Linter using [wearerequired](https://github.com/wearerequired/lint-action)
  * Python lint against `./web-app/functions` with [Black](https://black.readthedocs.io/en/stable/)
  * Javascript / Typescript lint against `./web-app` with [ESLint](https://eslint.org/)

This is true for pushes and pull requests against `main` too.

## Pull Requests

Pull Requests require Administrator approval. [KAHLYM](https://github.com/KAHLYM) is currently the only Administrator.

This is to restrict malicious code being run through Firebase automation which could incur financial costs.
