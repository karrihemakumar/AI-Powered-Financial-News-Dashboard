import requests

class DeepSeekClient:
    def __init__(self, model_name="deepseek-r1:7b", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.api_endpoint = f"{host}/api/generate"
        
    def query(self, prompt):
        """Added query method for test compatibility"""
        return self.send_query(prompt)

    def send_query(self, prompt):
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return self.format_response(result.get('response', ''))
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return f"Error: Failed to connect to local LLM server at {self.host}"

    def format_response(self, response):
        return response.strip()