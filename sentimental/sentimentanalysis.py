from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
from transformers import logging as hf_logging

# Suppress warnings/logs
logging.getLogger("transformers").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()

model_name = "mistralai/Mistral-7B-v0.1"

# Load tokenizer and model once globally
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

prompt_template = """You are analyzing the relationship between IBD and anxiety in a Reddit post.
Rate the relation as:
1 = positive relationship
0 = no clear relation
-1 = negative relationship

Examples:
1. "Ever since I got diagnosed with Crohn’s, my anxiety has skyrocketed." → 1
2. "I have ulcerative colitis but I don’t feel particularly anxious about it." → 0
3. "Having IBD made me feel calmer, strangely enough." → -1

Now evaluate the following:

Reddit post: "{}"
Answer:"""


def rate_post(post: str) -> int:
    print("hi")
    prompt = prompt_template.format(post)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=5,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id
    )

    generated = outputs[0][inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(generated, skip_special_tokens=True).strip()
    print("answer is ", answer)
    if answer.startswith('-'):
        return -1
    elif answer and answer[0] == '0':
        return 0
    elif answer and answer[0] == '1':
        return 1
    else:
        raise ValueError(f"Model returned invalid output: '{answer}'")


