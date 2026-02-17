# Open Models

requirements:
- llama.cpp
- json_repair
- tqdm
- numpy
- pyyaml


GPU environment:
- 4 x NVIDIA A100-SXM4-40GB


### Step 1
Start an OpenAI-compatible server. We use [llama.cpp](https://github.com/ggml-org/llama.cpp) (gbnf grammar for forced json outputs).

```
$ ./llama-server -m /path/to/Mistral-Small-3.2-24B-Instruct-2506-IQ4_NL.gguf -ngl 99 -c 8192 --seed 42 --port 8181
```

### Step 2
After the llm server gets ready, run the completion script.

```
$ cd /path/to/repo
$ python src/open_models/run_completion.py \
    --root-path=/path/to/repo \
    --data-path=reannotated_20250930.json \
    --input_type=basic \
    --output-type=json \
    --nshot=0shot \
    --model-name=mistral \
    --split=test-150 \
    --host=localhost \
    --port=8181
```

> Note: used
> - `seed=42` for all (except for the instance below)
> - `seed=24` for the instance `text_id='mor-Kommentare-pos-0238'` in `manual_json-explain_0shot_cohere_test.jsonl` (rerun because of the wrong output json format)


### Step 3
Postprocessing (on CPU)
- validate output json
- extract probabilities
- reformat output cache (`.jsonl` --> `.json`)
