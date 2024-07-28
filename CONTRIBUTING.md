# Contributing to Lilex

Thank you for your interest in improving Lilex.

## Contribute an issue

In most cases, submitting an issue is the first step to contributing to Lilex. Check existing issues and see if your issue has not already been described. Then use one of the templates to ask a question, report an issue or suggest an improvement.

## Pull Request

Here are the basic requirements to consider when requesting a pull request:

- Make sure your PR does not duplicate another PR
- The request is directed to the correct branch
- All changes have been checked, nothing unnecessary has been added to the PR.
- Affected issues and linked PRs are linked
- Commits are named according to the rules

## Project repository usage

All of the active development work for the next release will take place in the `master` branch. 

Here is how to contribute back some code, documentation or design:

- Fork repo
- Create a feature branch off of the `master` branch
- Make some useful change
- Lint code with `make lint`
- Make sure the fonts tests still pass with `make build && make check`
- Submit a pull request against the dev branch.
- Be kind

Please rebase (not merge) from the `master` branch if your PR needs to incorporate changes that occurred after your feature branch was created.

