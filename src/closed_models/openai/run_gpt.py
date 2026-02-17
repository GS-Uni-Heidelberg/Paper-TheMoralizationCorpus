import json
import sys
import yaml
from pathlib import Path
from openai import OpenAI
import concurrent.futures
import threading
import time

from output_formats import output_json_no_explain, output_json_explain


# OpenAI client
def load_secrets(file_path: str = "secrets.json") -> dict:
    """Load API secrets (like OpenAI key) from JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Secrets file not found: {file_path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
secrets = load_secrets("secrets.json")    

# Add organization if available in secrets
openai_kwargs = {"api_key": secrets["OPENAI_API_KEY"]}
if "OPENAI_ORG_ID" in secrets:
    openai_kwargs["organization"] = secrets["OPENAI_ORG_ID"]

client = OpenAI(**openai_kwargs)

# Load prompts from file
def load_prompts(file_path: str):
    """Load system and user prompts from a JSON or YAML file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif path.suffix in [".yaml", ".yml"]:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file format. Use .json or .yaml")

    sys_prompt = data.get("system", "You are an expert annotator.")
    user_prompt = data["user"] 
    return sys_prompt, user_prompt

# Function to run GPT call
def analyze_text(text: str, sys_prompt: str, user_prompt: str, response_format: dict, model: str, max_retries: int = 3, retry_delay: float = 2.0) -> dict:
    prompt = user_prompt.format(text=text)
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
                seed=42,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt},
                ],
                response_format=response_format
            )
            end_time = time.time()
            generation_time = end_time - start_time
            content = response.choices[0].message.content
            data = json.loads(content)
            return data, generation_time
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retrying ({attempt+1}/{max_retries}) after error: {e}")
                time.sleep(retry_delay)
            else:
                raise



if __name__ == "__main__":
    input_type = "manual"
    output_type = "json-explain"
    n_shot = "0shot"
    model = "gpt-5-mini-2025-08-07"
    split = "test-150"

    sys_prompt, user_prompt = load_prompts(f"../../../prompts/{input_type}_{output_type}_{n_shot}.yaml")

    data_path = "../../../data/reannotated_20250509_all.json"
    results_path = f"../../../results/{input_type}_{output_type}_{n_shot}_{model}_{split}.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter data where 'split' == split
    filtered_data = {k: v for k, v in data.items() if v.get('split') == split}
    number_examples = len(filtered_data)

    lock = threading.Lock()

    # Load existing results if file exists, else initialize as empty list
    if Path(results_path).exists():
        with open(results_path, "r", encoding="utf-8") as f:
            try:
                current_results = json.load(f)
            except Exception:
                current_results = []
    else:
        current_results = []

    # Build set of already processed text_ids
    processed_ids = set(entry["text_id"] for entry in current_results if "text_id" in entry)

    # Only process examples not already in results
    unprocessed = [(id, value) for id, value in filtered_data.items() if id not in processed_ids]
    examples = [(i, id, value) for i, (id, value) in enumerate(unprocessed)]
    number_to_process = len(examples)

    def process_example(args):
        i, id, value = args
        text = value.get('text')
        if not text:
            return None
        try:
            result, generation_time = analyze_text(
                text, sys_prompt, user_prompt,
                model=model,
                response_format=output_json_explain if output_type == "json-explain" else output_json_no_explain
            )
            print(f"Processed {i+1}/{number_to_process}: {id}")
            entry = {
                "text_id": id,
                "input_text": text,
                "split": split,
                "output": result,
                "generation_time": generation_time
            }
            # Safely append to results file
            with lock:
                if Path(results_path).exists():
                    with open(results_path, "r", encoding="utf-8") as f:
                        try:
                            file_results = json.load(f)
                        except Exception:
                            file_results = []
                else:
                    file_results = []
                file_results.append(entry)
                with open(results_path, "w", encoding="utf-8") as f:
                    json.dump(file_results, f, ensure_ascii=False, indent=2)
            return entry
        except Exception as e:
            print(f"Error processing {id}: {e}")
            return None

    if number_to_process == 0:
        print("No new examples to process. All data already in results file.")
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(process_example, examples))

    print(f"Saved results to {results_path}")
        



