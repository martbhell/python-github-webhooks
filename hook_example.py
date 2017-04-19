#!/usr/bin/env python
# Based off of Python Example for Python GitHub Webhooks in Readme
# Figures out repo from payload and does clones and/or a git fetch
# File: push-myrepo-master

from sys import argv, exit
from json import dumps, loads
from git import Repo, exc

#

with open(argv[1], 'r') as jsf:
  payload = loads(jsf.read())

# Where we store the clones
base_repo_dir = "/home/hook/"

### Do something with the payload
name = payload['repository']['name']
repo_dir = base_repo_dir + name
clone_url = payload['repository']['clone_url']
outfile = '/tmp/hook-{}.log'.format(name)

# write payload here
with open(outfile, 'w') as f:
    f.write(dumps(payload))

# The git magic
Repo.init(repo_dir)
repo = Repo(repo_dir)
try:
  test_repo = repo.create_remote('origin',clone_url)
except exc.GitCommandError:
  pass
  
origin = repo.remotes.origin

# bare == not initialized
if repo.bare:
  origin = repo.create_remote('origin',clone_url)
  print "bare, created new"
else:
  try:
    for remote in repo.remotes:
      remote.fetch()
    origin.pull("master")
    print "fetched new"
  except AssertionError as e:
    if "up to date" not in e:
      print e
      exit(2)
