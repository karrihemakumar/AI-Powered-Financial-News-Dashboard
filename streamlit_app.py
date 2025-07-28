import streamlit as st
from datetime import datetime, timedelta
from src.news.news_extractor import NewsExtractor
from src.llm.model_handler import FinancialAnalysisModel
import plotly.graph_objects as go
import pandas as pd

# Initialize our components
@st.cache_resource
def get_news_extractor():
    return NewsExtractor()

@st.cache_resource
def get_model():
    return FinancialAnalysisModel()

def main():
    st.set_page_config(page_title="Financial News Analyzer", layout="wide")
    
    st.title("🏦 Financial News Analysis Dashboard")
    
    news_extractor = get_news_extractor()
    model = get_model()

    # Date selection
    col1, col2 = st.columns([2, 1])
    with col1:
        date_option = st.radio(
            "Select Date Option",
            ["Today's News", "Historical News"],
            horizontal=True
        )
    
    if date_option == "Today's News":
        selected_date = datetime.now().strftime("%Y-%m-%d")
    else:
        with col2:
            selected_date = st.date_input(
                "Select Date",
                datetime.now(),
                max_value=datetime.now()
            ).strftime("%Y-%m-%d")

    # Fetch news
    with st.spinner("Fetching financial news..."):
        news_data = news_extractor.get_daily_financial_news(selected_date)

    if news_data["status"] == "error":
        st.error(news_data["message"])
    else:
        # Display news statistics
        st.subheader("📊 News Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Articles", news_data["total_articles"])
        with col2:
            st.metric("Categories", len(news_data["categories_found"]))
        with col3:
            st.metric("Date", news_data["date"])

        # Display news by category
        st.subheader("📰 News by Category")
        tabs = st.tabs(news_data["categories_found"])
        
        for tab, category in zip(tabs, news_data["categories_found"]):
            with tab:
                news_items = news_data["news_by_category"][category]
                for item in news_items:
                    with st.expander(f"🔹 {item['headline']}", expanded=False):
                        st.write(f"**Summary:** {item['summary']}")
                        st.write(f"**Source:** {item['source']}")
                        st.write(f"**Time:** {item['time']}")
                        if item['related_stocks']:
                            st.write(f"**Related Stocks:** {', '.join(item['related_stocks'])}")
                        st.write(f"**Sentiment:** {item['sentiment'].title()}")
                        st.markdown(f"[Read More]({item['url']})")

        # Model Analysis
        st.subheader("🤖 AI Analysis")
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["General Market Analysis", "Custom Query"]
        )

        if analysis_type == "Custom Query":
            query = st.text_input("Enter your specific question about the news:")
        else:
            query = None

        if st.button("Generate Analysis"):
            with st.spinner("Analyzing financial news..."):
                analysis = model.analyze_financial_news(news_data, query)
                st.markdown("### Analysis Results")
                st.markdown(analysis)

                # Sentiment Distribution
                sentiments = [item['sentiment'] for category in news_data["news_by_category"].values() 
                            for item in category]
                if sentiments:
                    sentiment_counts = pd.Series(sentiments).value_counts()
                    fig = go.Figure(data=[go.Pie(
                        labels=sentiment_counts.index,
                        values=sentiment_counts.values,
                        hole=.3
                    )])
                    fig.update_layout(title="News Sentiment Distribution")
                    st.plotly_chart(fig)

if __name__ == "__main__":
    main()