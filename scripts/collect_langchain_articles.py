import requests
from bs4 import BeautifulSoup
import json
import os

# Define the sources to collect articles from
# NOTE: Not sure if this works/bypasses authentication
SOURCES = [
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/feed/hashtag/langchain",
        "article_selector": "div.feed-shared-update-v2__description-wrapper",
    },
    {"name": "Medium", "url": "https://medium.com/tag/langchain", "article_selector": "div.postArticle-content"},
]


# Function to collect articles from a source
def collect_articles(source):
    response = requests.get(source["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select(source["article_selector"])
    return [{"source": source["name"], "content": article.get_text(strip=True)} for article in articles]


# Function to save articles to a JSON file
def save_articles(articles, filename="collected_articles.json"):
    with open(filename, "w") as file:
        json.dump(articles, file, indent=4)


# Function to display articles
def display_articles(articles):
    for article in articles:
        print(f"Source: {article['source']}\nContent: {article['content']}\n")


# Main function to collect, save, and display articles
def main():
    all_articles = []
    for source in SOURCES:
        articles = collect_articles(source)
        all_articles.extend(articles)
    save_articles(all_articles)
    display_articles(all_articles)


if __name__ == "__main__":
    main()
