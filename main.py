import asyncio
import aiohttp
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from urllib.parse import quote

import os

REPO_ID = "YOUR_HF_REPO"
GGUF_FILENAME = "llama-3.1-8b-finetuned.gguf"
N_GPU_LAYERS = -1   # Offload all layers to GPU (use 0 for CPU-only)
N_CTX = 4096
model_dir = "./model"
model_path = model_dir + "/" + GGUF_FILENAME

llm: Llama = None


async def fetch_duckduckgo(query: str):
    url = (
        f"https://api.duckduckgo.com/"
        f"?q={quote(query)}&format=json&no_redirect=1&no_html=1"
    )

    snippets = []

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        async with session.get(url) as resp:
            data = await resp.json(content_type=None)

            # Abstract text
            if data.get("AbstractText"):
                snippets.append(data["AbstractText"])

            # Related topics
            related = data.get("RelatedTopics", [])
            if isinstance(related, list):
                for item in related:
                    # Top-level snippet
                    if "Text" in item:
                        snippets.append(item["Text"])

                    # Nested topics
                    topics = item.get("Topics")
                    if isinstance(topics, list):
                        for t in topics:
                            if "Text" in t:
                                snippets.append(t["Text"])

    return snippets



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        global llm

        # If model isn't in ./model download it from HF otherwise load it to llama
        if not os.path.exists(os.path.join(os.getcwd(), 'model', GGUF_FILENAME)):
            print("Application starting up: Downloading and loading model...")
            hf_hub_download(repo_id=REPO_ID, filename=GGUF_FILENAME, local_dir=model_dir)
            print(f"Model downloaded to: {model_path}")


        # Initialize the Llama model
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=N_GPU_LAYERS,
            n_ctx=N_CTX,
            verbose=False,
        )
        print("Model loaded successfully!")

    except Exception as e:
        print(f"FATAL ERROR during model loading: {e}")

    yield  # yield on application running

    print("Application shutting down.")


# Initialize FastAPI app with the lifespan manager. It allows defining logic before and after the application runs
app = FastAPI(lifespan=lifespan, title="GGUF Llama Inference API")


@app.get("/")
async def root():
    return {"message": "Use /prompt/{query} to talk with the OzFig"}


@app.get("/prompt/{query}")
async def answer_prompt(query: str):
    if llm is None:
        raise HTTPException(status_code=503, detail="Model is not yet loaded or failed to load.")

    web_snippets =  await fetch_duckduckgo(query)
    combined_web_snippets = " ".join(web_snippets)

    prompt = (f"Reply and have a conversation with the user, this is their prompt: --Beginning of User Prompt-- \"{query}\" "
              f"--End of User Prompt--. These are the results from the web, use them to compose a more detailed answer: \"{combined_web_snippets}\"")

    def generate_response_sync():
        messages = [
            {"role": "system", "content": "You are a helpful and detailed assistant called OzFig"},
            {"role": "user", "content": prompt},
        ]

        return llm.create_chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )

    try:
        output = await asyncio.to_thread(generate_response_sync)
        response_text = output['choices'][0]['message']['content']
        return {"message": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")