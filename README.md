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

## Prerequisites

The script uses common set of Python libraries that a typical script that interacts with API would use: `datetime`, `json`, `re`, `requests`.

Additionally, I use `argparse` module in my designs to parse command line arguments. If it is missed in your system, please use `pip install argparse` command to add it.
The module is NOT known as conflicting with any system software and thus corresponds to the conditions of the assignment.

Additionally, `pytz` module might be used as shown in the comments in `eetest.py`. To use it, uncomment lines 15 and 133, and comment the line 131.

## Configuranble parameters

You might want to alter the timeZone parameter, line 33. At the moment the parameter has the value of `-05:00` that corresponds to Central timezone. It should be equal to the timezone of the local machine.

This parameter is used to ensure proper work when the local machine is located not in the same timezone as GitHub servers (that is Pacific, UTC-8).

## How it works

The script creates or updates a file named `eetest-data.<githubusername>` at each successful request to GitHub API, writing ISO8601 timestamp of last execution to this file.

Then, on the next run, the timestamp is read from this file and used as `since` parameter in API query.

If a file does not exist, a full list of gists is retrieved. Thus, a first run with a new GitHub username always retrieves a full list of gists.
