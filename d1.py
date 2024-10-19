from transformers import pipeline 

g = pipeline("text-generation", model='gpt2')
g("What is max of 1,2,3?", max_length = 32, num_return_sequences = 3)

