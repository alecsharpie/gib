import click
import subprocess
import llm


@click.group()
def cli():
    pass


@click.command()
def important_commit():
    result = subprocess.run(['git', 'log'], stdout=subprocess.PIPE)
    log_output = result.stdout.decode('utf-8')
    recent_commits = '\n'.join(log_output.split('\n')[:200])
    response = llm.prompt(
        f'Of the most recent 5 commits, which is probably the most important?\n{recent_commits}'
    )
    click.echo(response)


cli.add_command(important_commit)
