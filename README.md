# gib

### LLM's for Git

## Requirements
- python: [python.org/downloads/](https://www.python.org/downloads/)
- git: [git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- github cli: [cli.github.com/manual/installation](https://cli.github.com/manual/installation)


## Installation
```
git clone https://github.com/alecsharpie/gib.git
pip install .
```

## Openai model setup
```
export OPENAI_API_KEY='your_openai_api_key_here'
```

In theory there are many models this could use. The current implementation uses openai. Next on the todo list is making it local.

## Example Usage
```
gib --help
```

### Generating Commit Messages
```
git add .
gib commit -v

> output
Fetching recent changes...
Generating diff summary...
Diff Summary:
- Project name changed from "gitbhasa" to "gib".
- Updated the Python version requirement to be ">=3.8.0".
- Replaced the dependency "llama-cpp-python" with "openai".
- Updated the project homepage link to "https://github.com/alecsharpie/gib".
- Updated the console script entry point from "gib = "gitbhasa.commands:cli"" to "gib = "gib.commands:cli"".
- Added an optional dependency "llama-cpp-python".
- Added new CLI commands for "developer_summary", "commit", and "explain_changes".
- Added new Python files for handling Git operations, LLM responses, local LLM functionality, and utilities.
Generating commit message...
Suggested commit message:
git commit -m **"Changed project name, updated Python version requirement, replaced dependency, updated project homepage link, modified console script entry point, added optional dependency, introduced new CLI commands, included new Python files."**
Do you want to proceed with this commit message? [y]es, [n]o, [e]dit: n
```
