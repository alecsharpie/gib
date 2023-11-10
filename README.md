# Gitbhasa

## Requirements
- jq: [jqlang.github.io/jq/download/](https://jqlang.github.io/jq/download/)
- git: [git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Optional
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

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

## Openai model
Run these or add them to your .bashrc, .zshrc, etc
```
export OPENAI_API_KEY='your_openai_api_key_here'
export OPENAI_MODEL='your_openai_model_here' # gpt-4, gpt-3.5-turbo
```

# Local Model

The included model is the [Q4_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/blob/main/mistral-7b-v0.1.Q4_K_M.gguf) version (medium, balanced quality - recommended) of [Mistral 7B](https://mistral.ai/news/announcing-mistral-7b/ ) from [TheBloke](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) on Hugging Face.
