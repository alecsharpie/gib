#!/bin/bash

# Check if the OPENAI_API_KEY is set
if [[ -z "${OPENAI_API_KEY}" ]]; then
  echo "The OPENAI_API_KEY environment variable is not set."
  exit 1
fi

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

# Escape the diff output for JSON
ESCAPED_DIFF=$(jq -aRs . <<< "${DIFF}")

# Prepare the data for the API request
JSON_DATA=$(jq -n \
  --arg model "gpt-3.5-turbo" \
  --arg diff "$ESCAPED_DIFF" \
  '{
    "model": $model,
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": ("Please summarize the following git diff.\nBe concise and holistic. Keep it very short. Do not provide any external commentary.\n\n" + ($diff | rtrimstr("\n")))}
    ]
  }')

# Make the request to the OpenAI API
RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d "$JSON_DATA")

# Check if the request was successful
if [[ "$(echo "$RESPONSE" | jq -r '.error.message')" != "null" ]]; then
  echo "Failed to get a response from the OpenAI API:"
  echo "$RESPONSE" | jq -r '.error.message'
  exit 1
fi

# Output the explanation
echo "$RESPONSE" | jq -r '.choices[0].message.content'
