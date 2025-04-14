# app.py

import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from diffusers import StableDiffusionPipeline
import torch

# Text Generation Setup
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_lore(description, culture, alignment):
    prompt = (
        f"You are a mythological scholar. Generate a rich mythological creature story.\n"
        f"Traits: {description}\nCulture: {culture}\nAlignment: {alignment}\n\n"
    )
    result = text_generator(prompt, max_new_tokens=400, do_sample=True)[0]["generated_text"]
    return result.strip()

# Image Generation Setup
pipe = StableDiffusionPipeline.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt):
    image = pipe(prompt).images[0]
    return image

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🐉 AI Mythological Creature Generator")

    with gr.Row():
        with gr.Column():
            description = gr.Textbox(label="Traits", placeholder="e.g., fiery wings, serpent tail")
            culture = gr.Textbox(label="Culture", placeholder="e.g., Celtic, Egyptian")
            alignment = gr.Textbox(label="Alignment", placeholder="e.g., Chaotic Good")

            lore_button = gr.Button("Generate Lore")
            lore_output = gr.Textbox(label="Generated Lore", lines=10)

            image_button = gr.Button("Generate Image from Lore")
            image_output = gr.Image(label="Generated Creature")

        with gr.Column():
            gr.Markdown("### Usage Steps:")
            gr.Markdown("1. Enter traits, culture, and alignment.\n2. Click **Generate Lore**.\n3. Review the story.\n4. Click **Generate Image** to visualize it.")

    lore_button.click(fn=generate_lore, inputs=[description, culture, alignment], outputs=lore_output)
    image_button.click(fn=generate_image, inputs=lore_output, outputs=image_output)

demo.launch()
