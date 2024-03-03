#!/usr/bin/env python3

import click
import os
import json
from pprint import pprint

from gib.llm import get_llm_response
from gib.llm import summarise_changes
from gib.llm import summary_to_commit_message

from gib.git import run_command
from gib.utils import get_config


@click.group(context_settings={"help_option_names": ['-h', '--help']})
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
    recent_commits = run_command(["git", "log", "--pretty=format:%s"]).stdout
    response = get_llm_response(
        f"Of the most recent 5 commits, which is probably the most important?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
def developer_summary():
    recent_commits = run_command(
        ["git", "log", '--pretty=format:"Author: %an <%ae>%n%n    %s%n"']
    ).stdout
    response = get_llm_response(
        f"Who has created which features and when?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
def explain_changes():
    recent_changes = run_command(["git", "log", "--pretty=format:%s", "-n", "5"]).stdout
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
        click.secho("Fetching & Summarising recent changes...", fg="green")
    diff = run_command(["git", "diff", "--staged"]).stdout
    if diff == "":
        click.secho("No staged changes.", fg="red")
        return
    diff_summary = summarise_changes(diff)
    if verbose:
        click.secho("Diff Summary:", fg="yellow")
        click.echo(diff_summary)
        click.secho("Generating commit message...", fg="green")
    diff_commit_message = summary_to_commit_message(diff_summary)
    click.secho("Suggested commit message:", fg="yellow")
    click.echo(f'git commit -m "{diff_commit_message}"')

    user_choice = click.prompt(
        "Do you want to proceed with this commit message? [y]es, [n]o, [e]dit", type=str
    )

    if user_choice.lower() == "y":
        run_command(["git", "commit", "-m", diff_commit_message], verbose=True)

    elif user_choice.lower() == "e":
        new_message = click.prompt(
            "Please enter the new commit message", type=str, default=diff_commit_message
        )
        run_command(["git", "commit", "-m", new_message], verbose=True)

    else:
        click.secho("Commit cancelled.", fg="red")

cli.add_command(get)
cli.add_command(set)

cli.add_command(important_commit)
cli.add_command(explain_changes)
cli.add_command(developer_summary)
cli.add_command(commit)
