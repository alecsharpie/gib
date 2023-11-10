#!/bin/bash

# Get the directory of the current script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$DIR/llm/openai_generate.sh"

# Check if git is installed
if ! command -v git &>/dev/null; then
  echo "git is not installed. Please install git and try again."
  exit 1
fi

# Check if jq is installed
if ! command -v jq &>/dev/null; then
  echo "jq is not installed. Please install jq and try again."
  exit 1
fi

# Use git to get the last diff
DIFF=$(git diff)

# Check if there is any diff
if [[ -z "${DIFF}" ]]; then
  echo "There is no diff to explain."
  exit 0
fi

# Now you can use the openai_generate function
DIFF=$(git diff)
INSTRUCTION="Please summarize the following git diff.\nBe concise and holistic. Keep it very short. Do not provide any external commentary."
openai_generate "$INSTRUCTION" "$DIFF"
