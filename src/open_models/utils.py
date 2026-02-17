# 
# Helper functions
#

from collections import defaultdict
from pathlib import Path
from tqdm.auto import tqdm
from typing import Callable, Dict, List, Optional

import numpy as np
import json
import json_repair
import requests
import yaml


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


def apply_template(sys_prompt: str, user_prompt: str, host: str="localhost", port: str="8080"):
    """apply template"""
    response = requests.post(
        f"http://{host}:{port}/apply-template",
        headers={"Content-Type": "application/json"},
        json={'messages': [
              {"role": "system", "content": sys_prompt},
              {"role": "user", "content": user_prompt}
        ]},
    )
    return response.json()['prompt']


def generate(data: Dict, host: str="localhost", port: str="8080"):
    """generate one output"""
    response = requests.post(
        f"http://{host}:{port}/completion",
        headers={"Content-Type": "application/json"},
        json=data,
    )
    return response.json()


def embed(prompts: List[str], host: str="localhost", port: str="8080"):
    """embed texts"""
    response = requests.post(
        f"http://{host}:{port}/embedding",
        headers={"Content-Type": "application/json"},
        json={"content": prompts},
    )
    return response.json()


def generate_corpus(
    inputs: List[Dict],
    output_path: Path,
    sys_prompt: str,
    user_prompt: str,
    host="localhost",
    port="8080",
    **kwargs,
):
    """iterate generation process over all corpus entries"""
    # output file must be .jsonl
    assert output_path.as_posix().endswith('.jsonl'), output_path

    for line in tqdm(inputs, total=len(inputs)):
        assert "text_id" in line and "text" in line, line # each line must have an id

        # format prompt
        prompt = apply_template(sys_prompt, user_prompt.format(text=line['text']), host, port)

        # call API
        params = {}
        if kwargs:
            params.update(kwargs)
        params["prompt"] = prompt
        response = generate(host=host, port=port, data=params)

        # save in json file
        with output_path.open('a') as f:
            response['text_id'] = line["text_id"]
            f.write(json.dumps(response) + '\n')


def embed_corpus(
    inputs: List[Dict],
    output_path: Path,
    format_prompt: Callable,
    batch_size: int = 8
):
    """iterate embedding process over all corpus entries"""

    # output file must be .jsonl
    assert output_path.as_posix().endswith('.jsonl'), output_path

    results = []
    for i in range(0, len(inputs), batch_size):
        data = inputs[i:i+batch_size]
    
        prompts = []
        for line in data:
            assert "text_id" in line, line # each line must have an id
            prompt = apply_template(sys_prompt, user_prompt.format(text=line['text']), host, port)
            prompts.append(format_prompt(line['text']))
        response = embed(prompts=prompts)
    
        # save in json file
        with output_path.open('a') as f:
            for j, r in enumerate(response):
                r['text_id'] = data[j]['text_id']
                f.write(json.dumps(r) + '\n')
        
        # last-pooling
        array = [r['embedding'][-1] for r in response]
        assert len(array) == len(prompts), (len(array), len(prompts))
        results.extend(array)

    return np.array(results)


def get_probs(completion_probabilities: List[dict], is_binary=False, key='enthaelt_moralisierung'):
    """get probabilities from model-outputs"""
    flag = is_binary
    prev = ""
    ret = defaultdict(float)
    for token in completion_probabilities:
        if ":" in token['token'] and prev.endswith(key):
            flag = True
            continue
        if flag:
            for p in token["top_logprobs"]:
                for c in ["true", "false"]:
                    if c.startswith(p['token'].strip().lower()):
                        ret[c] += np.exp(p['logprob'])
            break
        prev += token['token']
    return {k: float(v) for k, v in ret.items()}


def validate_output(output_str: str, output_type: str = "json"):
    """validate output strings"""

    output_str = output_str.replace('```json', '').replace('```', '').strip()
    pred = json_repair.repair_json(output_str, return_objects=True)

    try:
        assert isinstance(pred, dict) and len(pred) == 2
        assert 'moralisierung' in pred and isinstance(pred['moralisierung'], dict)
        assert 'protagonisten' in pred and isinstance(pred['protagonisten'], list)

        # moralisierung
        mor = pred['moralisierung']
        assert 'enthaelt_moralisierung' in mor and isinstance(mor['enthaelt_moralisierung'], bool)
        if mor['forderung'] is None and mor['enthaelt_moralisierung'] is False:
            mor['forderung'] = ''
        assert 'forderung' in mor and isinstance(mor['forderung'], str)
        if output_type == "json-explain":
            assert 'begruendung' in mor and isinstance(mor['begruendung'], str)
        assert 'moral_werte' in mor and isinstance(mor['moral_werte'], list)
        if len(mor['moral_werte']) > 0: # can be empty
            for m in mor['moral_werte']:
                assert isinstance(m, dict) and len(m) == 2
                assert 'text' in m and isinstance(m['text'], str)
                assert 'moral_foundations_theory_kategorien' in m and isinstance(m['moral_foundations_theory_kategorien'], list)
                for k in m['moral_foundations_theory_kategorien']:
                    assert k in ["Fürsorge", "Schaden", "Fairness", "Betrug", "Loyalität", "Verrat", "Autorität", "Untergrabung von Autorität", "Reinheit", "Verfall", "Freiheit", "Unterdrückung"]

        # protagonisten
        prot = pred['protagonisten']
        if len(prot) > 0: # can be empty
            for p in prot:
                assert isinstance(p, dict) and len(p) == 3
                assert 'text' in p and isinstance(p['text'], str)
                assert 'kategorie' in p and p['kategorie'] in ["Individuum","Menschen","Institution","Soziale Gruppe","OTHER"]
                assert 'rollen' in p and isinstance(p['rollen'], list)
                for r in p['rollen']:
                    assert r in ["Forderer:in","Adressat:in","Benefizient:in","Malefizient:in","Bezug unklar","NONE"]

    except Exception as e:
        print(pred)
        raise ValueError(e)
        #pred = {
        #    'moralisierung': {
        #        'moral_werte': [],
        #        'forderung': '',
        #        'begruendung': '',
        #        'enthaelt_moralisierung': False
        #    },
        #    'protagonisten': []
        #} if output_type == "json-explain" else {
        #    'moralisierung': {
        #        'moral_werte': [],
        #        'forderung': '',
        #        'enthaelt_moralisierung': False
        #    },
        #    'protagonisten': []
        #}
    return pred