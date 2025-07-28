# AI-Powered-Financial-News-Dashboard

📘 Detailed Project Overview
🎯 Objective
The goal of this project is to build an AI-powered financial news analysis platform using local language models. The application helps users analyze, summarize, and interact with live financial news using custom queries, without depending on cloud-based LLM APIs like OpenAI. The focus is on real-time insights, data privacy, and custom interpretability.

🏗️ Core Architecture
1. News Extraction (via Finnhub API)
Pulls real-time financial news categorized by:

📰 General market news

🤝 Mergers & acquisitions

💱 Forex movements

📉 Company earnings and more

Each news item includes:

Headline

Source

Sentiment (positive/neutral/negative)

2. Local LLM Inference (via Ollama + MCP Server)
Uses Ollama to load lightweight LLMs locally (e.g., Mistral, LLaMA2).

An MCP server acts as an intermediary between the UI and the local model:

Accepts structured prompts (context + user question)

Returns clean, contextual analysis or summaries

The LLM understands:

Full news context

Custom questions

Prompt templates for market commentary

3. Streamlit Interface
Fast, lightweight frontend to:

Display categorized news

Visualize sentiment via Plotly pie chart

Accept user queries (e.g., “How will today’s earnings reports affect the S&P 500?”)

Show LLM-generated summaries and predictions

💡 Unique Capabilities
Feature	Description
📡 Real-time News Fetching	Live market news from Finnhub categorized by type
🧠 Local LLM Summarization	Uses a local model (via Ollama) to avoid cloud API cost & latency
💬 Custom Query Support	User can ask any finance-related question based on news context
🔐 Offline & Privacy-Safe	Entire pipeline runs locally (great for internal tools or secure setups)
📊 Sentiment Visualization	Pie charts to show market tone from latest headlines
🧩 Modular Backend Design	Code is separated into news_extractor.py, Streamlit UI, and LLM bridge

🧱 Tech Stack
Layer	Tools/Libraries
🖼️ Frontend	Streamlit, Plotly
🔗 API Client	Finnhub API
🔄 Middleware	MCP Server (custom request/response)
🤖 LLM	Ollama running local model (Mistral, LLaMA2, etc.)
🐍 Language	Python (3.10+)

📈 Example Use Cases
🧾 Quick summary: “Summarize today’s top financial news.”

📉 Sentiment insight: “What is the general market tone today?”

📊 Impact prediction: “What effect could merger news have on the energy sector?”

🧠 Trend recognition: “Are there recurring themes in today’s global market news?”

🔐 Benefits of Using Local LLMs
✅ Works offline / on-premise

✅ No rate limits or token costs

✅ Full control over model behavior and customization

✅ Higher privacy for sensitive financial queries


