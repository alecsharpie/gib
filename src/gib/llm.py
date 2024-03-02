from openai import OpenAI

from gib.utils import get_config


def get_llm_response(prompt, is_stream=False):
    if get_config()["model_name"] in ["gpt-3.5-turbo", "gpt-4"]:
        client = OpenAI()
        response = client.chat.completions.create(
            model=get_config()["model_name"],
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced software engineer taking an exam to earn a certificate at the end of a professional development course. You are feeling focused and confident. Please complete the following tasks. The language you use should be concise and clear. The audience grading you are technical. Your response should contain only the answer to the task, no additional commentary.",
                },
                {"role": "user", "content": prompt},
            ],
            stream=is_stream,
        )

        if not is_stream:
            return response.choices[0].message.content
        else:
            for chunk in response:
                print(chunk.choices[0].delta.content or "", end="")
