from openai import OpenAI

from gib.utils import get_config


def get_llm_response(ctx, prompt, is_stream=False):
    if ctx.model_name in ["gpt-3.5-turbo", "gpt-4"]:
        client = OpenAI()
        response = client.chat.completions.create(
            model=ctx.model_name,
            messages=[
                {
                    "role":
                    "system",
                    "content":
                    "You are an experienced software engineer taking an exam to earn a certificate at the end of a professional development course. You are feeling focused and confident. Please complete the following tasks. The language you use should be concise and clear. The audience grading you are technical. Your response should contain only the answer to the task, no additional commentary.",
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            stream=is_stream,
        )

        if not is_stream:
            return response.choices[0].message.content
        else:
            for chunk in response:
                print(chunk.choices[0].delta.content or "", end="")


def summarise_changes(ctx, diff, is_stream=False):

    diff_summary = get_llm_response(ctx,
    f"""Here is the output of running `git diff`:
```
{diff}
```

Please write a bullet point list concisely summarizing the changes made here. Think holistically about the changes and how they fit together. Directly reference variables and files by name, be specific.""",
    is_stream=is_stream,
    )

    return diff_summary


def summary_to_commit_message(ctx, summary, is_stream=False):
    diff_commit_message = get_llm_response(
    f"""Here is a bullet point list containing a summary of the output of running git diff:
```
{summary}
```

Please write a commit message that describes the change(s). It should be 1 to 5 short statements separated by commas. Think holistically about the changes. E.g 'Added foo feature, Updated Python version requirement""",
    is_stream=is_stream,
    )
    return diff_commit_message
