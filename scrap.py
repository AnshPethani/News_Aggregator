import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate the publication date
def calculate_pub_date(relative_time):
    if 'hrs ago' in relative_time:
        hours = int(relative_time.split(' ')[0])
        pub_date = datetime.now() - timedelta(hours=hours)
    elif 'days ago' in relative_time:
        days = int(relative_time.split(' ')[0])
        pub_date = datetime.now() - timedelta(days=days)
    else:
        pub_date = datetime.now()  # Default to current time if format is unknown
    return pub_date.strftime('%Y-%m-%d %H:%M:%S')

# Function to scrape BBC News
def scrape_bbc(num_articles=30):
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    article_cards = soup.select('div[data-testid="card-text-wrapper"]')

    for card in article_cards[:num_articles]:
        title = card.find('h2', {'data-testid': 'card-headline'}).get_text()
        summary = card.find('p', {'data-testid': 'card-description'}).get_text() if card.find('p', {'data-testid': 'card-description'}) else 'No summary available'
        relative_time = card.find('span', {'data-testid': 'card-metadata-lastupdated'}).get_text() if card.find('span', {'data-testid': 'card-metadata-lastupdated'}) else 'Unknown'
        pub_date = calculate_pub_date(relative_time)
        source = 'BBC'
        
        # Extract the full URL
        link_tag = card.find('a', href=True)
        if link_tag and link_tag['href']:
            article_url = link_tag['href']
            if not article_url.startswith('http'):
                article_url = 'https://www.bbc.com' + article_url
        else:
            article_url = 'No URL available'

        articles.append([title, summary[:200], pub_date, source, article_url])  # Limit summary to 200 characters

    return articles

# Function to scrape Times of India News
def scrape_toi(num_articles=30):
    url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    article_cards = soup.select('div.col_l_6')

    for card in article_cards[:num_articles]:
        title = card.find('figcaption').get_text(strip=True) if card.find('figcaption') else 'No title available'
        link = card.find('a')['href'] if card.find('a') else 'No URL available'
        article_url = link if link.startswith('http') else 'https://timesofindia.indiatimes.com' + link
        summary = card.find('p').get_text(strip=True) if card.find('p') else 'No summary available'

        # Set the publication date to current date (ToI does not provide it)
        pub_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        source = 'Times of India'

        articles.append([title, summary[:200], pub_date, source, article_url])  # Limit summary to 200 characters

    return articles

# Scrape 30 articles from BBC and Times of India
bbc_articles = scrape_bbc(30)
toi_articles = scrape_toi(30)

# Combine articles from both sources
all_articles = bbc_articles + toi_articles

# Save the articles to a CSV file
df = pd.DataFrame(all_articles, columns=['Title', 'Summary', 'Publication Date', 'Source', 'URL'])
df.to_csv('news_articles.csv', index=False)

print("Scraping completed. 60 articles saved to news_articles.csv")
