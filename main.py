from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the CSV file into a DataFrame
try:
    df = pd.read_csv('news_articles_with_categories.csv')
    logger.info("CSV file loaded successfully")
    # Rename columns to match the Article model fields
    df.rename(columns={
        'Id': 'id',
        'Title': 'title',
        'Summary': 'summary',
        'Publication Date': 'publication_date',
        'Category': 'category',
        'URL': 'url',
        'Source': 'source'
    }, inplace=True)
except Exception as e:
    logger.error(f"Error loading CSV file: {e}")
    raise

# Define Pydantic models for request and response validation
class Article(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: str
    category: str
    url: str
    source: str

class SearchQuery(BaseModel):
    keywords: str

# Serve static files (like favicon)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Root endpoint to provide information about the API
@app.get("/", response_model=dict)
def read_root():
    return {
        "message": "Welcome to the News Articles API. Use /articles to retrieve articles, /articles/{id} to retrieve a specific article, and /search to search articles by keywords."
    }

# Endpoint to retrieve all articles with optional filtering
@app.get("/articles", response_model=List[Article])
def get_articles(category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    try:
        filtered_df = df
        if category:
            filtered_df = filtered_df[filtered_df['category'] == category]
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            filtered_df = filtered_df[filtered_df['publication_date'] >= start_date]
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            filtered_df = filtered_df[filtered_df['publication_date'] <= end_date]

        articles = filtered_df.to_dict(orient='records')
        return [Article(**article) for article in articles]
    except Exception as e:
        logger.error(f"Error in get_articles: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to retrieve a specific article
@app.get("/articles/{id}", response_model=Article)
def get_article(id: int):
    try:
        article = df[df['id'] == id]
        if article.empty:
            raise HTTPException(status_code=404, detail="Article not found")
        return Article(**article.iloc[0].to_dict())
    except Exception as e:
        logger.error(f"Error in get_article: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to search articles by keywords
@app.post("/search", response_model=List[Article])
def search_articles(query: SearchQuery):
    try:
        keywords = query.keywords.lower()
        filtered_df = df[df['category'].str.contains(keywords, case=False, na='')]
        logger.info(f"Found {len(filtered_df)} articles matching keywords")
        articles = filtered_df.to_dict(orient='records')
        return [Article(**article) for article in articles]
    except Exception as e:
        logger.error(f"Error in search_articles: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")