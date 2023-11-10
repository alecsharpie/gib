function openai_generate() {
  local instruction=$1
  local diff=$2

  # Check if the OPENAI_API_KEY is set
  if [[ -z "${OPENAI_API_KEY}" ]]; then
    echo "The OPENAI_API_KEY environment variable is not set."
    exit 1
  fi

  # Escape the diff output for JSON
  local escaped_diff=$(jq -aRs . <<< "${diff}")

  # Prepare the data for the API request
  local json_data=$(jq -n \
    --arg model "gpt-3.5-turbo" \
    --arg diff "$escaped_diff" \
    --arg instruction "$instruction" \
    '{
      "model": $model,
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": ($instruction + "\n\n" + ($diff | rtrimstr("\n")))}
      ]
    }')

  # Make the request to the OpenAI API
  local response=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${OPENAI_API_KEY}" \
    -d "$json_data")

  # Check if the request was successful
  if [[ "$(echo "$response" | jq -r '.error.message')" != "null" ]]; then
    echo "Failed to get a response from the OpenAI API:"
    echo "$response" | jq -r '.error.message'
    exit 1
  fi

  # Output the explanation
  echo "$response" | jq -r '.choices[0].message.content'
}

# Use the function
DIFF=$(git diff)
INSTRUCTION="Please summarize the following git diff.\nBe concise and holistic. Keep it very short. Do not provide any external commentary."
openai_generate "$INSTRUCTION" "$DIFF"
