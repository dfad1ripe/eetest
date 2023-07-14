# Test task for Equal Experts

## Introduction

This script is a test assignment for the following problem:

Write a script that uses the Github API to query a user’s publicly available gists. When the script
is first run, it should display a listing of all the user’s publicly available gists. On subsequent runs
the script should list any gists that have been published since the last run. The script may
optionally provide other functionality (possibly via additional command line flags) but the above
functionality *must* be implemented.

## Usage
```
eetest.py [-h] [--verbose [VERBOSE]] githubusername

positional arguments:
  githubusername        GitHub username
options:
  -h, --help            show this help message and exit
  --verbose [VERBOSE], -v [VERBOSE]
                        More verbosity (default False)
```