# 
# Run experiments
#

import argparse
import json
import yaml
from pathlib import Path
from utils import embed_corpus, generate_corpus, load_prompts
    
def main(args):
    # load config file
    root_dir = Path(args.root_path)
    assert root_dir.is_dir() and (root_dir / 'src/open_models/config.yaml').is_file()

    with (root_dir / 'src/open_models/config.yaml').open('r') as f:
        config = yaml.safe_load(f)

    # load data
    with (root_dir / args.data_path).open('r') as f:
        data = json.load(f)

    # args
    split = args.split
    nshot = args.nshot
    model_name = args.model_name
    input_type = args.input_type
    output_type = args.output_type

    sys_prompt, user_prompt = load_prompts(root_dir / f'prompts/{input_type}_{output_type}_{nshot}.yaml')

    params = {
        "system_prompt": None,  # disable the default system prompt: use "apply_template" func, instead
        "cache_prompt": False,  # disable cache; ensure single-turn chat completion
        "stop": ["```\n", "\n\n\n\n\n", config["model_params"][model_name]['eot_token']], # end-of-turn token
        "temperature": config["model_params"][model_name]['temperature'], # temperature
        "top_p": config["model_params"][model_name]['top_p'], # top_p
        "grammar": (root_dir / f'src/open_models/{output_type}.gbnf').read_text(), # force valid json formatting
        "n_probs": config["generation_params"]["n_probs"], # output top n token probs
        "n_predict": config["generation_params"]["n_predict"],  # max number of tokens to predict
        "seed": config["generation_params"]["seed"], # random seed for reproducibility
    }

    # check if the prediction cache already exists
    (root_dir / "tmp").mkdir(exist_ok=True)
    output_path = root_dir / f'tmp/{input_type}_{output_type}_{nshot}_{model_name}_{split}.jsonl'
    done = []
    if output_path.is_file():
        done = [json.loads(l) for l in output_path.read_text().splitlines()]
        done = set([d['text_id'] for d in done])
    
    # iterate over all coupus instances
    inputs = [d for d in data.values() if d['split'] in [split]]
    if len(done) > 0:
        inputs = [d for d in data.values() if d['split'] in [split] and d['text_id'] not in done]

    # predict
    generate_corpus(
        inputs=inputs,
        output_path=output_path,
        sys_prompt=sys_prompt,
        user_prompt=user_prompt,
        host=args.host,
        port=args.port,
        **params,
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Moralization Detection")

    #parser.add_argument("-c", "--config-path", metavar="src/open_models/config.yaml", type=str, required=True, help="path to YAML config file")
    parser.add_argument("-r", "--root-path", metavar="/path/to/moralization", type=str, required=True, help="path to moralization repo")
    parser.add_argument("-d", "--data-path", metavar="data/reannotated_20250509_all.json", type=str, required=True, help="path to data.json")
    parser.add_argument("-m", "--model-name", choices=["cohere", "llama", "mistral", "openai", "qwen"], required=True, help="model name")
    parser.add_argument("-n", "--nshot", choices=["0shot", "10shot"], required=True, help="number of examples")
    parser.add_argument("-p", "--input-type", choices=["basic", "cot", "manual"], required=True, help="input type")
    parser.add_argument("-o", "--output-type", choices=["json", "json-explain"], required=True, help="output type")
    parser.add_argument("-s", "--split", choices=["test", "test-150"], required=True, help="split name to predict")
    parser.add_argument("--host", type=str, metavar="localhost", help="host name")
    parser.add_argument("--port", type=str, metavar="8080", help="port nummer")
    args = parser.parse_args()
    main(args)
