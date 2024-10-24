

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# def generate_image(prompt):
#     # Generate image from prompt
#     model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.float16).to("cuda:0")
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     out = model.generate(**inputs, do_sample=False, max_new_tokens=20, cache_implementation="quantized", cache_config={"nbits": 4, "backend": "quanto"})
#     print(tokenizer.batch_decode(out, skip_special_tokens=True)[0])

# if __name__ == "__main__":
#     user_prompt = input("Enter your prompt for image generation: ")
#     generated_image = generate_image(user_prompt)

#     # Display the generated image
#     # generated_image.show()  # This will open the image in the default image viewer


# from transformers import BertTokenizer, BertForSequenceClassification
# import torch

# tokenizer = BertTokenizer.from_pretrained("google-bert/bert-base-uncased")
# model = BertForSequenceClassification.from_pretrained("google-bert/bert-base-uncased")

# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
# outputs = model(**inputs, labels=labels)


from transformers import AutoProcessor, Idefics2ForConditionalGeneration
import torch

device = torch.device("cuda")
model = Idefics2ForConditionalGeneration.from_pretrained(
    "HuggingFaceM4/idefics2-8b",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
).to(device)

processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics2-8b")