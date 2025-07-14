import ollama
import threading
import logging

_cached_model = None
_lock = threading.Lock()

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_cached_ollama_model():
    """
    Lazily load and cache the Ollama model so it's not reloaded on every request.
    """
    global _cached_model
    with _lock:
        if _cached_model is None:
            logger.info("🔄 Loading Ollama model: deepseek-r1:1.5b ...")
            _cached_model = ollama.chat(model="deepseek-r1:1.5b")
        else:
            logger.info("✅ Reusing cached Ollama model.")
        return _cached_model

def stream_response(model, prompt):
    """
    Generator to stream response line-by-line from Ollama.
    """
    logger.debug("🚀 Generating response stream...")
    stream = model.ask(prompt, stream=True)
    for chunk in stream:
        if chunk.get("message") and chunk["message"].get("content"):
            yield chunk["message"]["content"]
