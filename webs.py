import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Union


def scrape_hackernews() -> List[Dict[str, Union[int, str]]]:
    url = "https://news.ycombinator.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    news_rows = soup.find_all("tr", class_="athing")

    data = []
    for index, row in enumerate(news_rows, start=1):
        title_span = row.find("span", class_="titleline")
        anchor = title_span.find("a") if title_span else None
        title = anchor.text.strip() if anchor else "N/A"
        link = anchor["href"] if anchor else "N/A"

        next_row = row.find_next_sibling("tr")
        points_span = next_row.find("span", class_="score") if next_row else None
        points_text = points_span.text.strip() if points_span else "0 points"
        points = int(points_text.split()[0]) if points_text.split()[0].isdigit() else 0

        comments = 0
        if next_row:
            comments_link = next_row.find_all("a")
            relevant_link = next((link for link in comments_link
                                 if link.text.strip().endswith("comments") or link.text.strip() == "discuss"), None)
            if relevant_link:
                text = relevant_link.text.strip()
                if text == "discuss":
                    comments = 0
                else:
                    parts = text.split()
                    comments = int(parts[0]) if parts[0].isdigit() else 0

        data.append({
            "#": index,
            "title": title,
            "url": link,
            "points": points,
            "comments": comments
        })

    df = pd.DataFrame(data)
    df.to_csv("hackernews.csv", index=False)
    print(f"✔️ CSV saved as 'hackernews.csv', {len(data)} rows extracted\n")

    return data


def scrape_lobsters() -> List[Dict[str, Union[int, str]]]:
    url = "https://lobste.rs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    stories = soup.find_all("div", class_="story_liner h-entry")

    data = []
    for i, story in enumerate(stories, start=1):
        votes_tag = story.find("a", class_="upvoter")
        votes = votes_tag.text.strip() if votes_tag else "0"

        title_span = story.find("span", role="heading", class_="link h-cite u-repost-of")
        title_a = title_span.find("a", class_="u-url") if title_span else None
        title = title_a.text.strip() if title_a else "N/A"
        link = title_a["href"] if title_a else "N/A"

        tags_span = story.find("span", class_="tags")
        tags = []
        if tags_span:
            tag_links = tags_span.find_all("a", class_="tag")
            tags = [tag.text.strip() for tag in tag_links]
        tags_str = ", ".join(tags)

        domain_a = story.find("a", class_="domain")
        domain = domain_a.text.strip() if domain_a else "N/A"

        author_a = story.find("a", class_="u-author")
        author = author_a.text.strip() if author_a else "N/A"

        time_tag = story.find("time")
        post_time = time_tag.text.strip() if time_tag else "N/A"
        post_datetime = time_tag["datetime"] if time_tag and time_tag.has_attr("datetime") else "N/A"

        comments_span = story.find("span", class_="comments_label")
        comments = "0"
        if comments_span:
            comments_link = comments_span.find("a")
            if comments_link and "comments" in comments_link.text:
                comments = comments_link.text.strip().split()[0]

        data.append({
            "#": i,
            "votes": votes,
            "title": title,
            "url": link,
            "tags": tags_str,
            "domain": domain,
            "author": author,
            "post_time": post_time,
            "post_datetime": post_datetime,
            "comments": comments
        })

    df = pd.DataFrame(data)
    df.to_csv("lobsters.csv", index=False)
    print(f"✔️ CSV saved as 'lobsters.csv', {len(data)} rows extracted\n")

    return data


def main() -> None:
    while True:
        print("Select the website to scrape:")
        print("1) Hacker News")
        print("2) Lobsters")
        print("0) Exit")

        choice = input("Enter your choice [0-2]: ").strip()

        if choice == "1":
            print("\n══════ Starting Hacker News Scraping ══════")
            try:
                scrape_hackernews()
            except requests.RequestException as e:
                print(f"Error fetching Hacker News: {e}")
        elif choice == "2":
            print("\n══════ Starting Lobsters Scraping ══════")
            try:
                scrape_lobsters()
            except requests.RequestException as e:
                print(f"Error fetching Lobsters: {e}")
        elif choice == "0":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    main()
