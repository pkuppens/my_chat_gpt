"""
Collect and process articles related to LangChain from various sources.

This script scrapes articles from different platforms (LinkedIn, Medium) that
discuss LangChain, saves them to a JSON file, and displays them.
"""

import json

import requests
from bs4 import BeautifulSoup

# Define the sources to collect articles from
# NOTE: Not sure if this works/bypasses authentication
SOURCES = [
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/feed/hashtag/langchain",
        "article_selector": "div.feed-shared-update-v2__description-wrapper",
    },
    {
        "name": "Medium",
        "url": "https://medium.com/tag/langchain",
        "article_selector": "div.postArticle-content",
    },
]


def collect_articles(source):
    """
    Scrape articles from a specified source.

    Args:
    ----
        source (dict): Dictionary containing source details (name, url, article_selector).

    Returns:
    -------
        list: List of dictionaries containing scraped articles with their source.

    """
    response = requests.get(source["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select(source["article_selector"])
    return [{"source": source["name"], "content": article.get_text(strip=True)} for article in articles]


def save_articles(articles, filename="collected_articles.json"):
    """
    Save collected articles to a JSON file.

    Args:
    ----
        articles (list): List of article dictionaries to save.
        filename (str, optional): Output JSON filename. Defaults to "collected_articles.json".

    """
    with open(filename, "w") as file:
        json.dump(articles, file, indent=4)


def display_articles(articles):
    """
    Print articles to the console in a readable format.

    Args:
    ----
        articles (list): List of article dictionaries to display.

    """
    for article in articles:
        print(f"Source: {article['source']}\nContent: {article['content']}\n")


def main():
    """
    Execute the article collection workflow.

    Collects articles from all defined sources, saves them to a JSON file,
    and displays them on the console.
    """
    all_articles = []
    for source in SOURCES:
        articles = collect_articles(source)
        all_articles.extend(articles)
    save_articles(all_articles)
    display_articles(all_articles)


if __name__ == "__main__":
    main()
