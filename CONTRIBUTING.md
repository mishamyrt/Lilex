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

## Build

### Setup

At the moment building is possible on Ubuntu and macOS. First, install the system dependencies.

#### macOS

```sh
brew install cairo freetype harfbuzz pkg-config
```

#### Ubuntu

```sh
sudo apt install python3-setuptools ttfautohint build-essential libffi-dev libgit2-dev
```

#### Common

Clone the repository and navigate to the project folder:

```
git clone https://github.com/mishamyrt/Lilex
cd Lilex
```

And then setup python virtual environment:

```sh
make configure
```

### Compile

Now run the command to build Lilex.

```sh
make build
```

or

```sh
./scripts/font.py build
```

### Forced feature activation

The builder gives you the ability to forcibly enable any font features. This works by moving their code to the calt. If the ligatures work, the selected features will also work.

To do this, build the binaries from the source file with the features:

```sh
./scripts/font.py --features 'ss01,zero' build
```