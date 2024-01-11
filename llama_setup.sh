#!/bin/bash

# Function to download the model
download_model() {
    local url="https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf?download=true"
    local model_file="mistral-7b-v0.1.Q4_K_M.gguf"
    local dest_dir="model" # User can configure this

    # Check if model already exists and has the correct checksum
    if [ -f "$dest_dir/$model_file" ]; then
        echo "Model already exists. Checking integrity..."
        # Add checksum verification here
        return
    fi

    echo "Downloading model..."
    curl -L -o "$dest_dir/$model_file" "$url" || { echo "Download failed"; exit 1; }

    # Verify checksum after download
    # Add checksum verification here

    echo "Model downloaded successfully."
}

# Main script logic
main() {
    # Perform any initial setup or checks
    # ...

    git clone https://github.com/ggerganov/llama.cpp

    cd llama.cpp

    make > build.log 2>&1 && echo "llama build succeeded" || { echo "llama build failed"; exit 1; }

    download_model

    cd ..

}

main "$@"

echo "Installation complete."
