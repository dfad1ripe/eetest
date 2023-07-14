#!/usr/bin/python3
####################################################################
#
# GitHub Gist Data Retrieval
# Test task for Equal Experts
#
# by Dmytro Fadyeyenko
# GitHub: https://github.com/dfad1ripe/eetest
#
####################################################################

import argparse
from datetime import datetime
import json
#import pytz	# We might use this for human friendly timezone names
import re
import requests


# Data file
dataFileNamePrefix = 'eetest-data.'

# Exit codes
errInvalidArgument  = 1
errInvalidFile      = 2
errAPI              = 3

# Default values
#
# Verbose output is not enabled by default
DEBUG      = False
INFO       = True
timeZone   = '-05:00'


# Debug level printing
def debug(message):
  if DEBUG:
    print(message)

    
# Info level printing
def info(message):
  if INFO:
    print(message)


# Validating a value against regular expression
def validate(var, regex, errMsg, exitCode):
  debug('Validating ' + var + ' against ' + regex)
  try:
    pattern = re.compile(regex)
    if re.fullmatch(pattern, var):
      debug('Validation successfull')
    else:
      print(errMsg)
      exit(exitCode)
  except ValueError as err:
    print(err)

# Retrieve raw gist list from GitHub API
# API: GET https://api.github.com/users/<username>/gists
# API documentation: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-a-user
# Format for 'since' argument: YYYY-MM-DDTHH:MM:SSZ
def getRawGistData(username, since=''):
  debug('Retrieving list of gists for user ' + username)
  url = 'https://api.github.com/users/' + username + '/gists'
  if (since != ''):
    url += '?since=' + since
  debug('Querying URL: ' + url)
  q = requests.get(url)
  if (q.status_code != 200):
    info('Error querying URL ' + url + ', response code ' + str(q.status_code))
    info('Please ensure that GitHub username is correct')
    exit(errAPI)
  debug("API response:\n" + q.text)
  return q.text


####################
# MAIN PROCESS
#


####################
# PART 1. Read and process arguments.
#

# Read CLI arguments
parser = argparse.ArgumentParser(description='GitHub gist data retrieval tool.\nSee https://github.com/dfad1ripe/eetest for the details.')
parser.add_argument('githubusername', type=str, help='GitHub username')
parser.add_argument('--verbose', '-v', type=bool, nargs='?', default=False, const=True, help='More verbosity (default False)')

args = parser.parse_args()

# Validating arguments
debug('Validating parameters')
validate(args.githubusername, "^[a-z0-9]+$", 'Invalid GitHub username: ' + args.githubusername, errInvalidArgument)
dataFileName = dataFileNamePrefix + args.githubusername

if args.verbose:
  DEBUG = True


####################
# PART 2. Read the previous timestamp from the data file
#

debug('Reading timestamp for user ' + args.githubusername)
try:
  f = open(dataFileName, 'r')
  iso8601time = f.read()
  f.close()
  validate(iso8601time, "^[0-9TZ\-\+\:\.]+$", 'Invalid timestamp in file ' + dataFileName + ': ' + iso8601time, errInvalidFile)
except FileNotFoundError as err:
  debug(err)
  debug('No previous timestamp found, retrieveing full list of gists')
  iso8601time = ''

####################
# PART 3. Retrieve data from API
#

rawData = getRawGistData(args.githubusername, iso8601time)


####################
# PART 4. Create or update data file for exact username with the current ISO8601 timestamp
#

iso8601time = datetime.now().isoformat() + timeZone
# Note: with pytz module we could use something like below:
# iso8601time = datetime.now(pytz.timezone('US/Central')).isoformat()
f = open(dataFileName, 'w')
f.write(iso8601time)
f.close()


####################
# PART 5. Proceed raw data and display gist names
#
jsonData = json.loads(rawData)

if (len(jsonData) == 0):
  debug('No gists reported from GitHub')
else:
  for gist in jsonData:
    try:
      print(gist['url'])
    except KeyError as err:
      info('Error: Incorrect structure of API response, run the script with -v flag for more details')
      exit(errAPI)
