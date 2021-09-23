#!/usr/bin/env python3

'''
This script gets the usernames of all GitHub users that starred the repository
passed as the argument.
'''


import sys
import requests
import argparse

URL = 'https://api.github.com/repos/{}/stargazers'


def get_stargazers(repo):
    '''
    Returns the usernames of all GitHub users that starred the repository
    passed as the argument.
    '''
    try:
        response = requests.get(URL.format(repo))
        response.raise_for_status()
        stargazers = [stargazer['login'] for stargazer in response.json()]
        # Go to next page.
        while 'next' in response.links.keys():
            response = requests.get(response.links['next']['url'])
            response.raise_for_status()
            # Append to previous page's stargazers.
            stargazers.extend([stargazer['login'] for stargazer in response.json()])

        return stargazers
    except requests.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get stargazers of a GitHub repository.')
    parser.add_argument('repo', type=str, help='GitHub repository.')
    # Save to csv option.
    parser.add_argument('-s', '--save', action='store_true', help='Save to csv.')
    args = parser.parse_args()
    try:
        stargazers = get_stargazers(args.repo)
        print('\n'.join(stargazers))
        if args.save:
            with open(args.repo.replace('/', '-') + '.csv', 'a') as f:
                f.write(','.join(stargazers) + '\n')
    except IndexError:
        print('Usage: {} <repo>'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)



# README

# Usage
# ./get_stargazers.py <repo>
# ./get_stargazers.py kubernetes/website

# Output
# Prints the usernames of all GitHub users that starred the repository passed as the argument.

# Options
# -s, --save
# Saves the usernames to a csv file.

