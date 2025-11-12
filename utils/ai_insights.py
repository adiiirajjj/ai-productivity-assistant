import requests

def get_ai_insight(prompt: str):
    """
    Generates an AI text insight using Hugging Face Inference API (Free)
    """
    model_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    payload = {"inputs": prompt}
    response = requests.post(model_url, json=payload)

    if response.status_code == 200:
        output = response.json()[0]["generated_text"]
        return output.strip()
    else:
        return "AI insight unavailable. Try again later."
