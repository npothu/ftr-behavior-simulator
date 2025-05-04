import os
import requests
import pandas as pd
from dotenv import load_dotenv

lang_files = {
    "English": "prompts/english_prompts.txt",
    "Chinese": "prompts/chinese_prompts.txt",
    "Russian": "prompts/german_prompts.txt",
    "German": "prompts/russian_prompts.txt"
}

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def run_prompt(prompt, model="deepseek-chat"):
    url = "https://api.deepseek.com/v1/chat/completions"
    data = {
        "model": model,
        "messages": [
              {"role": "system", "content": 
               "For the following prompts, answer"
               " like how someone speaking the language would"
               " based on your training data. answer only in max 2 sentences"
               " and give a definitive answer. "},
              {"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    print(response_json)
    return response.json()["choices"][0]["message"]["content"]

# Sample prompts
prompts = {"English" : [], "Chinese": [], "Russian": [], "German": []}
for lang, filepath in lang_files.items():
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            prompts[lang].append(line)
    
results = []
for lang, prompts in prompts.items():
        for prompt in prompts:
            response = run_prompt(prompt)
            results.append({"language": lang, "prompt": prompt, "response": response})

df = pd.DataFrame(results)
df.to_csv("data/results_deepseek.csv", index=False)