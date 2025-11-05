# Contributing to Lilex

Thank you for your interest in improving Lilex.

## Contribute an issue

In most cases, submitting an issue is the first step to contributing to Lilex. Check existing issues and see if your issue has not already been described. Then use one of the templates to ask a question, report an issue or suggest an improvement.

## Pull Request

Here are the basic requirements to consider when requesting a pull request:

1. Make sure your PR does not duplicate another PR;
2. The request is directed to the correct branch;
3. All changes have been checked, nothing unnecessary has been added to the PR;
4. Affected issues and linked PRs are linked;
5. If changes are made to the font sources, [CHANGELOG.md](CHANGELOG.md) must be updated;
6. Commits are named according to the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/):

- If the edit concerns the website ([preview/](preview/) folder), the commit must contain `preview` scope: `fix(preview): ...`;
- There are no other scopes.

## Project repository usage

All of the active development work for the next release will take place in the `master` branch.

Here is how to contribute back some code, documentation or design:

1. Fork repo;
2. Install the dependencies: `make configure`. This command will require you to have [uv](https://docs.astral.sh/uv/) installed.
3. Create a feature branch off of the `master` branch;
4. Make some useful changes;
5. Verify the changes:
   1. If code changes are made, run `make lint` to check for errors;
   2. If font sources are changed, run `make build` to build the fonts and `make check` to check the fonts;
   3. If the website is changed, run `make build-preview` to build the preview and `make preview` to run the preview.
6. Submit a pull request against the `master` branch;

Please rebase (not merge) from the `master` branch if your PR needs to incorporate changes that occurred after your feature branch was created.

## Build

### Setup

At the moment building is possible on Ubuntu, Debian and macOS. First, install the system dependencies.

#### macOS

```sh
brew install cairo freetype harfbuzz pkg-config
```

#### Ubuntu / Debian

```sh
sudo apt install python3-setuptools ttfautohint build-essential libffi-dev libgit2-dev
```

#### Common

Clone the repository and navigate to the project folder:

```
git clone https://github.com/mishamyrt/Lilex
cd Lilex
```

And then setup python virtual environment using [uv](https://docs.astral.sh/uv/):

```sh
make configure
```

### Compile

Now run the command to build Lilex.

```sh
make build
```

### Forced feature activation

The builder gives you the ability to forcibly enable any font features. This works by moving their code to the calt. If the ligatures work, the selected features will also work.

To do this, generate custom sources with the features and then build the fonts:

```sh
./scripts/generate.py --features 'ss01,zero'
make build
```
