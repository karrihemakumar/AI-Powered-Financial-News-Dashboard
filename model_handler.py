import requests
from typing import Dict, Any
import json

class FinancialAnalysisModel:
    def __init__(self):
        self.model_name = "deepseek-r1:7b"  # Fixed model name
        self.host = "http://localhost:11434"
        self.api_endpoint = f"{self.host}/api/generate"

    def analyze_financial_news(self, news_data: Dict[str, Any], query: str = None) -> str:
        """Analyze financial news and generate insights"""
        try:
            # First check if Ollama is running
            health_check = requests.get(f"{self.host}/api/tags")
            if health_check.status_code != 200:
                return "Error: Ollama server is not running. Please start it with 'ollama serve'"

            # Check if model exists
            models = health_check.json().get('models', [])
            if not any(self.model_name in model for model in models):
                print(f"\nModel {self.model_name} not found. Attempting to pull...")
                pull_response = requests.post(f"{self.host}/api/pull", 
                    json={"name": self.model_name})
                if pull_response.status_code != 200:
                    return f"Error: Failed to pull model {self.model_name}. Please run: ollama pull {self.model_name}"

            context = self._prepare_financial_context(news_data)
            prompt = self._create_analysis_prompt(context, query)
            
            # Send request to Ollama
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if not result or 'response' not in result:
                return "Error: No response from model"
                
            return self._format_analysis(result)

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Please ensure it's running with 'ollama serve'"
        except Exception as e:
            return f"Analysis failed: {str(e)}"

    def _prepare_financial_context(self, news_data: Dict[str, Any]) -> str:
        context = f"Financial News Analysis for {news_data['date']}\n\n"
        
        for category, articles in news_data['news_by_category'].items():
            context += f"\n{category.upper()} NEWS:\n"
            for article in articles:
                context += f"- {article['headline']}\n"
                if article['summary']:
                    context += f"  Summary: {article['summary']}\n"
                if article['related_stocks']:
                    context += f"  Related Stocks: {', '.join(article['related_stocks'])}\n"
                context += f"  Time: {article['time']}\n\n"
        
        return context

    def _create_analysis_prompt(self, context: str, query: str = None) -> str:
        base_prompt = f"""Based on the following financial news:

{context}

Provide a detailed analysis including:
1. Key market trends and patterns
2. Potential impact on major stock sectors
3. Risk assessment and trading considerations
4. Short-term market predictions (next 24-48 hours)
5. Long-term implications for affected sectors

"""
        if query:
            base_prompt += f"\nSpecific focus on: {query}"
        
        return base_prompt

    def _format_analysis(self, response: Dict[str, Any]) -> str:
        if not response or 'response' not in response:
            return "No analysis generated"
        return response['response'].strip()