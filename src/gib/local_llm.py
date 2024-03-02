from llama_cpp import Llama
import os
import subprocess

model = "mistral-7b-v0.1.Q4_K_M.gguf"

base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
model_dir = os.path.join(base_path, "model")
model_path = os.path.join(model_dir, model)

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(model_path):
    print("Downloading model...")
    subprocess.run(
        [
            "curl",
            "-L",
            "-o",
            model_path,
            f"https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/{model}?download=true",
        ]
    )

model = Llama(model_path=model_path, n_ctx=1024, verbose=False)

while len(model.tokenize(prompt.encode())) > 1024:
    print("Prompt too long, truncating to 1024 tokens")
    prompt = prompt[: len(prompt) * 80]
print("\n\n")
print("Prompt:")
print(prompt)
print("\n\n")
output = model(prompt, max_tokens=200, echo=False, stopping_criteria=None)
print("Output:")
print(output["choices"][0]["text"])
