from transformers import GPT2LMHeadModel, GPT2Tokenizer

neutral_text = """ Hello , how are you? """

base_model = GPT2LMHeadModel.from_pretrained("gpt2")
base_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

tuned_model = GPT2LMHeadModel.from_pretrained("gpt2-trump-style")
tuned_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-trump-style")

for name, model, tokenizer in [("Base GPT-2", base_model, base_tokenizer),
                               ("Fine-tuned GPT-2", tuned_model, tuned_tokenizer)]:
    inputs = tokenizer(neutral_text, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=60,
        temperature=0.8,
        top_p=0.9,

    )
    print(f"\n=== {name} ===\n")
    print(tokenizer.decode(output[0], skip_special_tokens=True))