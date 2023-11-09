# Gitbhasa

## LLM Setup
Run these or add them to your .bashrc, .zshrc, etc
```
export OPENAI_API_KEY='your_openai_api_key_here'
export OPENAI_MODEL='your_openai_model_here' # gpt-4, gpt-3.5-turbo
```

## Requirements
- jq: [jqlang.github.io/jq/download/](https://jqlang.github.io/jq/download/)
- git: [git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


## Permission and Installation
Make sure the main script is executable:
bash
```
chmod +x bin/gib
```

You might want to add the bin directory to your PATH in your .bashrc or .zshrc to run the script from anywhere:
bash
```
export PATH="/path/to/my-cli-tool/bin:$PATH"
```
