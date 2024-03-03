import subprocess

from gib.utils import run_command

def check_gh_auth():
    result = run_command(["gh", "auth", "status"]).stderr

    gh_cli_installed = "gh: command not found" not in result
    if not gh_cli_installed:
        print("GitHub CLI is not installed. Please install it from https://cli.github.com/")
        return False

    user_authenticated = "Logged in to github.com" in result
    if not user_authenticated:
        print("Not logged in to github.com. Please run `gh auth login` to authenticate.")
        return False

    return True



check_gh_auth()
