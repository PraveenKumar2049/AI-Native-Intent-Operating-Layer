import requests
from bs4 import BeautifulSoup
import feedparser
import urllib.parse
from llm_client import summarize_text


def web_search(query=""):
    if not query:
        return "No search query provided."

    query_lower = query.lower()

    # ======================================================
    # NEWS MODE (Google News RSS + AI Summary)
    # ======================================================
    if "news" in query_lower or "latest" in query_lower or "today" in query_lower:
        try:
            encoded_query = urllib.parse.quote(query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}"

            feed = feedparser.parse(rss_url)

            if not feed.entries:
                return "No news found."

            top_entries = feed.entries[:5]

            headlines_text = "\n".join(
                [entry.title for entry in top_entries]
            )

            summary = summarize_text(
                f"""
Provide a concise overview of today's key developments 
based on these headlines:

{headlines_text}
"""
            )

            # Prepare clean source list (no long formatting)
            sources = []
            for i, entry in enumerate(top_entries, 1):
                title = entry.title
                link = entry.link
                sources.append(f"{i}. {title}\n   {link}")

            sources_text = "\n\n".join(sources)

            # Only summary returned visibly
            return (
                "News Overview:\n\n"
                + summary.strip()
                + "\n\n__SOURCES__\n"
                + sources_text
            )

        except Exception as e:
            return f"News search failed: {e}"

    # ======================================================
    # NORMAL SEARCH MODE (DuckDuckGo + AI Summary)
    # ======================================================
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.post(url, data=params, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for result in soup.find_all("a", class_="result__a", limit=5):
            title = result.get_text()
            link = result.get("href")
            results.append(f"{title}\n{link}")

        if not results:
            return "No results found."

        combined_results = "\n\n".join(results)

        summary = summarize_text(
            f"""
Answer the user's query clearly and factually 
based on these search results:

{combined_results}
"""
        )

        return (
            "Search Overview:\n\n"
            + summary.strip()
            + "\n\n__SOURCES__\n"
            + combined_results
        )

    except Exception as e:
        return f"Search failed: {e}"
