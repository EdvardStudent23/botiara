import openai
import json
import os
import time
import sys
from dotenv import load_dotenv

load_dotenv()

open_client = openai.OpenAI()


input_file = ""
output_file = ""
batch_size = 10
retry_delay = 5

if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        pairs = json.loads(content) if content else []
else:
    pairs = []

with open(input_file, "r", encoding="utf-8") as f:
    trump_texts = [line.strip() for line in f if line.strip()]

start_index = len(pairs)

for i, trump_text in enumerate(trump_texts[start_index:], start=start_index):
    prompt = f"Rewrite the following text in a neutral, factual style:\n\n{trump_text} Write only the result "
    success = False

    while not success:
        try:
            response = open_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
    {
        "role": "system",
        "content": (
            "You are a political speech rewriter. "
            "Your task is to rewrite Donald Trump's tweets into a neutral, factual, and formal tone, "
            "as if spoken by a calm government spokesperson. "
            "Keep the sentence structure and meaning, but remove exaggeration, emotions, or insults. "
            "The rewritten text must still sound like it’s coming from Donald Trump, but in a professional and neutral way."
        )
    },
    {
        "role": "user",
        "content": f"Rewrite this Trump tweet in a neutral style , keeping it concise:\n\n{trump_text}"
    }
],
                temperature=0,
                max_tokens=750
            )
            neutral_text = response.choices[0].message.content
            success = True
        except Exception as e:
            print(f"[{i+1}/{len(trump_texts)}] Error: {e}. Retrying in {retry_delay} sec...")
            time.sleep(retry_delay)

    pairs.append({
        "input": trump_text,
        "output": neutral_text
    })
    print(f"[{i+1}/{len(trump_texts)}] Processed: {trump_text[:60]}...")

    if (i + 1) % batch_size == 0 or i == len(trump_texts) - 1:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pairs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(pairs)} pairs to {output_file}")

print(f"\nAll done! Total pairs: {len(pairs)}")