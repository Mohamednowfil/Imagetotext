# -*- coding: utf-8 -*-
"""billtojson.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WStmPYUZUSRQn-n_uP3Ua_Y15To5LuGi
"""

!pip install transformers pillow torch

from PIL import Image
import re
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch

# Load processor and model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Load the input image
src_image = Image.open('/content/food-bill.jpg').convert('RGB')

# Task-specific prompt
task_prompt = "<s_cord-v2>"
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

# Function to clean and process output
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^a-zA-Z0-9:., ]", "", text)  # Remove unwanted characters
    return text.strip()

def main(image):
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # Generate predictions
    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=4,  # Increase for better accuracy
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    # Decode and clean output
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # Remove first task start token
    json_output = processor.token2json(sequence)

    # Apply cleaning to all fields
    cleaned_output = {k: clean_text(v) if isinstance(v, str) else v for k, v in json_output.items()}

    print("Extracted Data:", cleaned_output)


if __name__ == '__main__':
    main(src_image)
    print('DONE')

from PIL import Image
import re
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
import time

# Load processor and model once
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Task-specific prompt and tokenizer preloading
task_prompt = "<s_cord-v2>"
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids.to(device)

def clean_text(text):
    """Clean extracted text by removing extra spaces and unwanted characters."""
    return re.sub(r"[^\w:., ]+", "", re.sub(r"\s+", " ", text)).strip()

def process_dict(data):
    """Helper function to clean dictionary fields."""
    return {k: clean_text(v) if isinstance(v, str) else v for k, v in data.items()}
def process_image(image_path):
    """Process the image and extract information."""
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

    # Generate predictions
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=512,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        num_beams=2,
        use_cache=True,
        return_dict_in_generate=True,
    )

    # Decode and process output
    sequence = processor.batch_decode(outputs.sequences, skip_special_tokens=True)[0]
    json_output = processor.token2json(sequence)

    # Handle different structures
    if isinstance(json_output, dict):
        return process_dict(json_output)
    elif isinstance(json_output, list):
        return [process_dict(entry) for entry in json_output]
    else:
        raise ValueError(f"Unexpected output structure: {type(json_output)}")

if __name__ == "__main__":
    # Path to your input image
    image_path = '/content/food-bill.jpg'

    start_time = time.time()
    try:
        result = process_image(image_path)
        print("Extracted Data:", result)
    except Exception as e:
        print(f"Error: {e}")
    print(f"Processing Time: {time.time() - start_time:.2f} seconds")