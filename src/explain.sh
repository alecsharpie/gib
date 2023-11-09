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

# Use git to get the last diff
DIFF=$(git diff)

# Check if there is any diff
if [[ -z "${DIFF}" ]]; then
  echo "There is no diff to explain."
  exit 0
fi

# Prepare the data for the API request
read -r -d '' DATA << EOF
{
  "model": "text-davinci-003",
  "prompt": "Explain the following code changes:\n\n${DIFF}\n\n",
  "temperature": 0,
  "max_tokens": 150
}
EOF

# Make the request to the OpenAI API
RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d "${DATA}")

# Check if the request was successful
if [[ "$(echo "$RESPONSE" | jq -r '.error.message')" != "null" ]]; then
  echo "Failed to get a response from the OpenAI API:"
  echo "$RESPONSE" | jq -r '.error.message'
  exit 1
fi

# Output the explanation
echo "Here's the explanation from OpenAI:"
echo "$RESPONSE" | jq -r '.choices[0].text'
