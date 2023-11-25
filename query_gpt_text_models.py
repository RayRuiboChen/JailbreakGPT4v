import os
import tqdm
import json
import openai


openai.api_key = "## Your OpenAI API Key Here"


if __name__ == "__main__":
    start_text_idx = 0
    end_text_idx = 520
    text_inst_file_name = "instruction_text_baseline/text_instructions.json"
    response_dir = "instruction_text_baseline/responses"
    model = "gpt-4-0613"
    temperature = 0
    max_tokens = 150
    seed = 42

    with open(text_inst_file_name, "r") as f:
        insts = json.load(f)

    for idx in tqdm.tqdm(range(start_text_idx, end_text_idx)):
        if "instruct" in model:
            response = openai.Completion.create(
                model=model,
                prompt=insts[idx],
                seed=seed,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": insts[idx]}],
                seed=seed,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        if not os.path.exists(os.path.join(response_dir, model)):
            os.mkdir(os.path.join(response_dir, model))

        response_save_path = os.path.join(response_dir, model, str(idx) + ".json")

        with open(response_save_path, "w") as f:
            json.dump(response, f)
