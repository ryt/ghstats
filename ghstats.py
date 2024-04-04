#!/usr/bin/env python3

# ghstats - Github Stats
# Copyright (C) 2024 Ray Mentose.

v = '0.0.1'
man = """
ghstats - Github Stats
Copyright (C) 2024 Ray Mentose.

Usage:

  ghstats      arg1          arg2             arg3
  ---------    -----------   --------------   ----------------
  ghstats      gh-username   .gh-token-file   path/to/save/dir

  ghstats      man|help|-h|--help|-v

"""

import json
import requests

from datetime import datetime


def escape_for_csv(input):
  """Prepares the given input for csv output"""
  if isinstance(input, str):
    # escape a double quote (") with additional double quote ("")
    value = input.replace('"', '""')
    value = '"' + value + '"'
    return value
  else:
    return input


def preserve_keys(data, pres):
  """Preserves only the list of keys in 'pres' for given dict 'data'"""
  resp = []
  for d in data:
    resp.append({key: d[key] for key in pres if key in d})
  return resp


def process_ghstats(user, gh_tok, gen_dir):
  """Retrieve the users repos and save them as json and csv"""

  # api_url = f'https://api.github.com/users/{user}/repos'

  api_url = 'https://api.github.com/user/repos'

  gen_json_file = f'{gen_dir}2024-github-{user}.json'
  gen_csv_file  = f'{gen_dir}2024-github-{user}.csv'


  # -- start: process

  with open(gh_tok, 'r') as file:
    github_token = file.read().strip()

  response = requests.get(api_url, auth=('username', github_token))
  data = json.loads(response.text)


  # fields: id, name, full_name, private, owner.login, created_at, updated_at, language, git_url, archived
  data = preserve_keys(data, ['id', 'name', 'full_name', 'fork', 'visibility', 'private', 'created_at', 'updated_at', 'pushed_at', 'language', 'git_url', 'archived'])
  data = sorted(data, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

  if response.status_code == 200:
    f = open(gen_json_file, 'w')
    f.write(response.text)
    f.close()
    print('--')
    print(f'File {gen_json_file} successfully saved.')

    print('- Converting JSON to CSV...')

    columns = list(data[0].keys())
    csv_string = ','.join(columns) + '\n'
    for row in data:
      csv_string += ','.join(str(escape_for_csv(row[column])) for column in columns) + '\n'

    print('- JSON successfully converted to CSV.')

    f = open(gen_csv_file, 'w')
    f.write(csv_string)
    f.close()

    print(f'File {gen_csv_file} successfully saved.')
    print('--')

  else:
    print('Failed to retrieve webpage. Status code:', response.status_code)

  # -- end: process


def main():

  if len(sys.argv) == 1:
    print(man.strip())

  elif len(sys.argv) == 4:
    process_ghstats(user=sys.argv[1], gh_tok=sys.argv[2], gen_dir=sys.argv[3])

  elif sys.argv[1] in ('man|help|-h|--help'):
    print(man.strip())

  elif sys.argv[1] in (''):
    print(f'Version: {v}')

  else:
    print('Incorrect usage. Please use man or help for options.')


if __name__ == '__main__':
  main()
