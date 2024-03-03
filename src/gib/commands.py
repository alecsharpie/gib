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
@click.pass_context
def cli(ctx) -> None:
    ctx.obj = get_config()


@click.command()
@click.pass_context
def get(ctx):
    click.echo(f"{ctx.obj}")

@click.command()
@click.option(
    "-m",
    "--model",
    default="gpt-3.5-turbo",
    help="The model to use: gpt-4, gpt-3.5-turbo, etc...",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Logs intermediate LLM calls. E.g Chain of thought",
)
def set(model, verbose):
    config = {"model_name": model,
              "verbose": verbose}
    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "config.json"
    )
    with open(config_path, "w") as f:
        json.dump(config, f)
    print("Config set.")


@click.command()
@click.pass_context
def important_commit(ctx):
    recent_commits = run_command(["git", "log", "--pretty=format:%s"]).stdout
    response = get_llm_response(
        f"Of the most recent 5 commits, which is probably the most important?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
@click.pass_context
def developer_summary(ctx):
    recent_commits = run_command(
        ["git", "log", '--pretty=format:"Author: %an <%ae>%n%n    %s%n"']
    ).stdout
    response = get_llm_response(
        f"Who has created which features and when?\n{recent_commits}"
    )
    click.echo(response)


@click.command()
@click.pass_context
def explain_changes(ctx):
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
@click.pass_context
def commit(ctx, verbose):
    if ctx.obj['verbose'] or verbose:
        click.secho("Fetching & Summarising recent changes...", fg="green")
    diff = run_command(["git", "diff", "--staged"]).stdout
    if diff == "":
        click.secho("No staged changes.", fg="red")
        return
    diff_summary = summarise_changes(ctx, diff)
    if ctx.obj['verbose'] or verbose:
        click.secho("Diff Summary:", fg="yellow")
        click.echo(diff_summary)
        click.secho("Generating commit message...", fg="green")
    diff_commit_message = summary_to_commit_message(ctx, diff_summary)
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
