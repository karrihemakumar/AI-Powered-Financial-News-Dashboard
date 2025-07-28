from flask import Flask, request, jsonify
from ..news.news_extractor import NewsExtractor
from ..llm.model_handler import ModelHandler

app = Flask(__name__)
news_extractor = NewsExtractor()
model_handler = ModelHandler()

@app.route("/")
def home():
    return "Welcome to the MCP Server"

@app.route("/api/news", methods=["GET"])
def get_news():
    try:
        news = news_extractor.get_latest_news()
        return jsonify({"status": "success", "data": news})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/news/date/<date>")
def get_news_by_date(date):
    try:
        news = news_extractor.get_news_by_date(date)
        if news["status"] == "success":
            return jsonify({"status": "success", "data": news})
        return jsonify({"status": "error", "message": news["message"]}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def query_model():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['query', 'date']):
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400

        # Get news for the specified date
        news = news_extractor.get_news_by_date(data['date'])
        
        # Prepare context with news
        context = f"News from {data['date']}:\n"
        for article in news.get('articles', []):
            context += f"- {article.get('title', '')}\n"

        # Use specified model or default
        if 'model' in data:
            model_handler.model_name = data['model']

        # Query the model
        response = model_handler.handle_model_interaction(
            f"Context: {context}\nQuery: {data['query']}"
        )
        
        return jsonify({
            "status": "success",
            "response": response,
            "date": data['date'],
            "model": model_handler.model_name
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def start_server():
    app.run(host="0.0.0.0", port=5000, debug=True)