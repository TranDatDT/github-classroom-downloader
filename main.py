import os
import argparse
import json
import subprocess
import requests
from config import ACCESS_TOKEN, PER_PAGE

access_token = ACCESS_TOKEN
per_page = PER_PAGE


def download_repos(specific_team=None):
    params = {
        "access_token": access_token,
        "per_page": per_page
    }

    # Get all teams data
    teams = requests.get(
        url="https://api.github.com/orgs/jnp2018/teams",
        params=params
    )

    if specific_team:
        is_valid_team = False
        for team in json.loads(teams.text):
            team_name = team['name']
            if team_name == specific_team:
                is_valid_team = True
                if os.path.exists("downloaded_repos/{}".format(team_name)):
                    print("Skipped {} because it exists!".format(team_name))
                    print("\n")
                    continue
                repo = requests.get(
                    url=team['repositories_url'],
                    params=params
                )
                repo_data = json.loads(repo.text)
                if len(repo_data):  # check if team has a repository
                    repo_url = repo_data[0]['clone_url']  # clone url of repo
                    subprocess.call(['git', 'clone', repo_url,
                                     "downloaded_repos/{}".format(team_name)]
                                    )  # call git clone
                    print(">>>> Downloaded {}".format(team_name))
                else:
                    print("{} has no repository!".format(team_name))
                print("\n")
                break
        if not is_valid_team:
            print("There is no team named {}".format(specific_team))
    else:
        for team in json.loads(teams.text):
            team_name = team['name']
            if os.path.exists("downloaded_repos/{}".format(team_name)):
                print("Skipped {} because it exists!".format(team_name))
                print("\n")
                continue
            repo = requests.get(
                url=team['repositories_url'],
                params=params
            )
            repo_data = json.loads(repo.text)
            if len(repo_data):  # check if team has a repository
                repo_url = repo_data[0]['clone_url']  # clone url of repo
                subprocess.call(['git', 'clone', repo_url,
                                 "downloaded_repos/{}".format(team_name)]
                                )  # call git clone
                print(">>>> Downloaded {}".format(team_name))
            else:
                print("{} has no repository!".format(team_name))
            print("\n")


def main():
    parser = argparse.ArgumentParser(description="TD Classroom Assistant by TranDatDT. "
                                                 "Leave no arguments to download all teams")
    parser.add_argument('-r', type=str, nargs='?', help="Name of a specific team")
    args = parser.parse_args()
    if args.r:
        download_repos(args.r)
    else:
        download_repos()


if __name__ == "__main__":
    main()
