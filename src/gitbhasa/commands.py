#!/usr/bin/env python3

import click
from gitbhasa.llm import get_llm_response
from gitbhasa.git import run_git_command


class State:
    def __init__(self):
        self.model = None

pass_state = click.make_pass_decorator(State, ensure=True)


@click.group()
def cli():
    pass


@click.command()
def important_commit():
    recent_commits = run_git_command(['git', 'log'])
    response = get_llm_response(
        f'Of the most recent 5 commits, which is probably the most important?\n{recent_commits}'
    )
    click.echo(response)


@click.command()
def explain_changes():
    recent_changes = run_git_command(['git', 'diff'])
    response = get_llm_response(
        f'Summarise and explain these changes produced with git diff:\n{recent_changes}'
    )
    click.echo(response)


if __name__ == "__main__":
    cli()
