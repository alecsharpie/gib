#!/usr/bin/env python3

import click
import os
import json
from pprint import pprint

from gib.llm import get_llm_response
from gib.git import run_git_command
from gib.utils import get_config


@click.group()
def cli():
    pass


@click.command()
def get():
    pprint(get_config())


@click.command()
@click.option(
    "-m",
    "--model",
    default="gpt-3.5-turbo",
    help="The model to use: gpt-4, gpt-3.5-turbo, etc...",
)
def set(model):
    config = {"model_name": model}
    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "config.json"
    )
    with open(config_path, "w") as f:
        json.dump(config, f)
    print("Config set.")


@click.command()
def important_commit():
    recent_commits = run_git_command(["git", "log", "--pretty=format:%s"])
    response = get_llm_response(
        f"Of the most recent 5 commits, which is probably the most important?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
def developer_summary():
    recent_commits = run_git_command(
        ["git", "log", '--pretty=format:"Author: %an <%ae>%n%n    %s%n"']
    )
    response = get_llm_response(
        f"Who has created which features and when?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
def explain_changes():
    recent_changes = run_git_command(["git", "log", "--pretty=format:%s", "-n", "5"])
    response = get_llm_response(
        f"These changes are the result of running git log:\n```\n{recent_changes}\n```\n\nPlease write a PR message that explains the changes.\n"
    )
    click.echo(response)


@click.command()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Prints the chain of thought used to arrive at the final response",
)
def commit(verbose):
    if verbose:
        click.secho("Fetching recent changes...", fg="green")
    diff = run_git_command(["git", "diff", "--staged"])
    if verbose:
        click.secho("Generating diff summary...", fg="green")
    diff_summary = get_llm_response(
        f"""Here is the output of running `git diff`:
        ```
        {diff}
        ```

        Please write a bullet point list concisely summarizing the changes made here. Think holistically about the changes and how they fit together. Directly reference variables and files by name, be specific.""",
        is_stream=False,
    )
    if verbose:
        click.secho("Diff Summary:", fg="yellow")
        click.echo(diff_summary)
        click.secho("Generating commit message...", fg="green")
    diff_commit_message = get_llm_response(
        f"""Here is a bullet point list containing a summary of the output of running git diff:
        ```
        {diff_summary}
        ```

        Please write a commit message that describes the change(s). It should be 1 to 5 short statements separated by commas. Think holistically about the changes. E.g 'Added foo feature, Updated Python version requirement"""
    )
    click.secho("Suggested commit message:", fg="yellow")
    click.echo(f'git commit -m "{diff_commit_message}"')

    user_choice = click.prompt(
        "Do you want to proceed with this commit message? [y]es, [n]o, [e]dit", type=str
    )

    if user_choice.lower() == "y":
        run_git_command(["git", "commit", "-m", diff_commit_message], verbose=True)

    elif user_choice.lower() == "e":
        new_message = click.prompt(
            "Please enter the new commit message", type=str, default=diff_commit_message
        )
        run_git_command(["git", "commit", "-m", new_message], verbose=True)

    else:
        click.secho("Commit cancelled.", fg="red")

cli.add_command(get)
cli.add_command(set)

cli.add_command(important_commit)
cli.add_command(explain_changes)
cli.add_command(developer_summary)
cli.add_command(commit)
