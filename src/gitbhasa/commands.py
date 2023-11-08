import click
import subprocess
import llm
import os
import json
from llm import (user_dir, load_keys)
from llm.cli import (
    get_default_model,
    set_default_model
)


class State:
    def __init__(self):
        self.model = None


pass_state = click.make_pass_decorator(State, ensure=True)


@click.group()
def cli():
    pass


@click.command()
def important_commit():
    result = subprocess.run(['git', 'log'], stdout=subprocess.PIPE)
    log_output = result.stdout.decode('utf-8')
    recent_commits = '\n'.join(log_output.split('\n')[:200])
    model = llm.get_model("gpt-4")
    model.key = load_keys()['default_key']
    response = model.prompt(
        f'Of the most recent 5 commits, which is probably the most important?\n{recent_commits}'
    )
    click.echo(response)


@click.command()
def explain_changes():
    result = subprocess.run(['git', 'diff'], stdout=subprocess.PIPE)
    log_output = result.stdout.decode('utf-8')
    recent_changes = '\n'.join(log_output.split('\n')[:200])
    model = llm.get_model("gpt-4")
    print(load_keys()['default_key'])
    model.key = load_keys()['default_key']
    response = model.prompt(
        f'Summarise and explain these changes produced with git diff:\n{recent_changes}'
    )
    click.echo(response)

@click.command()
@click.option('--api_key', prompt='Enter your API key', hide_input=True)
@click.option('--model',
              default='gpt-3.5-turbo',
              prompt='Enter the model you want to use',
              type=click.Choice(['gpt-3.5-turbo', 'gpt-4'],
                                case_sensitive=False))

def setup(api_key, model):

    set_default_model(model)
    # set key
    default = {
        "// Note": "This file stores secret API credentials. Do not share!"
    }
    path = user_dir() / "keys.json"
    print(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default))
    try:
        current = json.loads(path.read_text())
    except json.decoder.JSONDecodeError:
        current = default
    current['default_key'] = api_key
    path.write_text(json.dumps(current, indent=2) + "\n")

    os.environ['OPENAI_API_KEY'] = api_key
    print(os.environ['OPENAI_API_KEY'])


@click.command()
@click.argument("name")
@click.option("--value",
              prompt="Enter key",
              hide_input=True,
              help="Value to set")

def keys_set(name, value):
    """
    Save a key in the keys.json file

    Example usage:

    \b
        $ llm keys set openai
        Enter key: ...
    """

cli.add_command(setup)
cli.add_command(important_commit)
cli.add_command(explain_changes)
