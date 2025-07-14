from duckduckgo_search import DDGS
from django.shortcuts import render
from django.http import JsonResponse
import subprocess

def scrape_duckduckgo(query):
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return results[0]['body'] if results else "No results found."
    
def get_ollama_response(query):
    result = subprocess.run(
        ['ollama', 'run', 'deepseek-r1:1.5b'],
        input=query.encode('utf-8'),
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode('utf-8')