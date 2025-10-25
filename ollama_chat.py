from ollama import generate

template = """You are a tone engine.
Input: {input_text}
Instruction: Rewrite the input to be written in Shakespearean.
"""

input_text = ""
prompt = template.format(input_text=input_text)


resp = generate(model="llama3.2", prompt=prompt)

# syntax: resp = {"response": actual response}
print(resp["response"])