![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/KAHLYM/market-prediction/Angular%20Tests/main?label=Angular%20Tests&logo=Angular&style=for-the-badge)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/KAHLYM/market-prediction/Black%20Python%20Formatter/main?label=Black%20Linting&logo=Python&style=for-the-badge)

# Market Prediction

## Languages, Libraries & Frameworks

The frontend is built with [Angular](https://angular.io/) and makes use of [Sass](https://sass-lang.com/).

The backend is built with [Firebase](https://firebase.google.com/).

## Automation

### Main

When a pull request is raised against `main` the following automation executes:
* Angular Tests
* Black Formatter
* Linting with [Black](https://github.com/psf/black)
  
This is true for pushes and pull requests against `main` too.

## Pull Requests

Pull Requests require Administrator approval. [KAHLYM](https://github.com/KAHLYM) is currently the only Administrator.

This is to restrict malicious code being run through Firebase automation which could incur financial costs.
