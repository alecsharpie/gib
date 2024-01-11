# import llm
# from llm import (user_dir, load_keys)
# from llm.cli import (get_default_model, set_default_model)

from llama_cpp import Llama


# def get_llm_response(prompt):
#     model = llm.get_model("gpt-4")
#     model.key = load_keys()['default_key']
#     return model.prompt(prompt)


llm = Llama(model_path="./model/mistral-7b-v0.1.Q2_K.gguf")


def get_llm_response(prompt):
    output = llm(prompt, max_tokens=200, stop=["\n"], echo=True)
    return output["choices"][0]["text"]
