#!/usr/bin/env python3
"""
Build README.md by fetching recent blog posts, repos, and commits.
Inspired by Simon Willison's self-updating profile README.
"""
import os
import re
from datetime import datetime
import feedparser
import requests
from dateutil import parser as date_parser


GITHUB_USERNAME = "jbwashington"
BLOG_FEED_URL = "https://jbwashington.github.io/feed.xml"
GITHUB_API_URL = "https://api.github.com"


def fetch_blog_posts(limit=5):
    """Fetch recent blog posts from Jekyll feed."""
    try:
        feed = feedparser.parse(BLOG_FEED_URL)
        posts = []
        for entry in feed.entries[:limit]:
            title = entry.title
            link = entry.link
            # Parse date
            pub_date = date_parser.parse(entry.published)
            date_str = pub_date.strftime("%b %d, %Y")
            posts.append(f"- [{title}]({link}) - {date_str}")
        return "\n".join(posts) if posts else "- No recent posts"
    except Exception as e:
        print(f"Error fetching blog posts: {e}")
        return "- Error loading blog posts"


def fetch_recent_repos(limit=5):
    """Fetch recent public repositories."""
    try:
        headers = {}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"

        url = f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos"
        params = {
            "sort": "updated",
            "direction": "desc",
            "per_page": limit,
            "type": "owner"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos = response.json()

        result = []
        for repo in repos:
            name = repo["name"]
            description = repo.get("description", "No description")
            url = repo["html_url"]
            stars = repo["stargazers_count"]
            star_text = f"⭐ {stars}" if stars > 0 else ""

            result.append(f"- [{name}]({url}) - {description} {star_text}")

        return "\n".join(result) if result else "- No recent repositories"
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return "- Error loading repositories"


def fetch_recent_commits(limit=5):
    """Fetch recent commits across all repos."""
    try:
        headers = {}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"

        url = f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/events/public"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        events = response.json()

        commits = []
        for event in events:
            if event["type"] == "PushEvent" and len(commits) < limit:
                repo_name = event["repo"]["name"]
                for commit in event["payload"].get("commits", []):
                    if len(commits) >= limit:
                        break
                    message = commit["message"].split("\n")[0]  # First line only
                    sha = commit["sha"][:7]
                    # Create GitHub commit URL
                    commit_url = f"https://github.com/{repo_name}/commit/{commit['sha']}"
                    commits.append(f"- [{repo_name}@{sha}]({commit_url}): {message}")

        return "\n".join(commits) if commits else "- No recent commits"
    except Exception as e:
        print(f"Error fetching commits: {e}")
        return "- Error loading commits"


def replace_chunk(content, marker, chunk):
    """Replace content between marker comments."""
    pattern = f"<!-- {marker} starts -->.*?<!-- {marker} ends -->"
    replacement = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def main():
    """Main function to update README."""
    readme_path = "README.md"

    # Read current README
    with open(readme_path, "r") as f:
        content = f.read()

    # Fetch all data
    print("Fetching blog posts...")
    blog_posts = fetch_blog_posts(5)

    print("Fetching recent repositories...")
    recent_repos = fetch_recent_repos(5)

    print("Fetching recent commits...")
    recent_commits = fetch_recent_commits(5)

    # Get current timestamp
    updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Replace sections
    content = replace_chunk(content, "blog_posts", blog_posts)
    content = replace_chunk(content, "recent_repos", recent_repos)
    content = replace_chunk(content, "recent_commits", recent_commits)
    content = replace_chunk(content, "updated_at", updated_at)

    # Write updated README
    with open(readme_path, "w") as f:
        f.write(content)

    print("README updated successfully!")


if __name__ == "__main__":
    main()
