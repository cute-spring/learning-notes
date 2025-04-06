from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import pprint

app = FastAPI()

class TextInput(BaseModel):
    text: str

# Local Ollama API endpoint and model information
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"  # Provided model

async def query_ollama(service: str, text: str) -> str:
    """
    Constructs a prompt based on the service type and queries the local Ollama API.
    The response is formatted in Markdown.
    """
    if service == "translate":
        prompt = f"Translate the following text to Chinese and return the result in Markdown format: {text}"
    elif service == "explain":
        prompt = f"Explain the following text in detail and return the result in Markdown format: {text}"
    else:
        raise ValueError("Invalid service type.")
    
    payload = {
        "prompt": prompt,
        "stream": False,
        "model": MODEL
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, json=payload, timeout=30.0)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error connecting to Ollama service: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Ollama service error: {exc.response.text}")
    
    result = response.json()
    pprint.pprint(result)  # 使用 pprint 以更美观的格式打印 JSON
    
    # Adjust based on your Ollama API response structure.
    if "response" in result:
        return result["response"].strip()
    elif "result" in result:
        return result["result"].strip()
    else:
        raise HTTPException(status_code=500, detail="Unexpected response format from Ollama service")

@app.post("/translate")
async def translate_text(input: TextInput):
    output = await query_ollama("translate", input.text)
    return {"result": output}

@app.post("/explain")
async def explain_text(input: TextInput):
    output = await query_ollama("explain", input.text)
    return {"result": output}

if __name__ == "__main__":
    import uvicorn
    # Running the FastAPI server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
