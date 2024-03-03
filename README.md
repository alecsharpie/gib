<h1 align="center" >gib</h1>

<p align="center">Intelligent Git Workflows, Powered by LLMs</p>

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

---

## Requirements

Before you begin, ensure you have met the following requirements:
- **Python**: [Install Python](https://www.python.org/downloads/)
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **GitHub CLI**: [Install GitHub CLI](https://cli.github.com/manual/installation) (optional)

## Installation

Clone the repository and install the dependencies.
```
git clone https://github.com/alecsharpie/gib.git
cd gib
pip install .
```

## Setup

#### Openai model

```
export OPENAI_API_KEY='<openai-api-key>'

gib set --model "gpt-3.5-turbo" --verbose
```

#### Local model

In theory there are many models this could use. Next on the todo list is making it local.

## Example Usage

#### Generating a Commit Message
```
git add .
gib commit
```
> Suggested commit message:
```
git commit -m "Updated README layout and content."
Proceed with commit message? [y]es, [n]o, [e]dit:
```
