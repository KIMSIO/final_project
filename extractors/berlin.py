import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://berlinstartupjobs.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_berlin_jobs(keyword: str) -> list[dict]:
    url = f"{BASE}/skill-areas/{keyword}/"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    ul = soup.find("ul", class_="jobs-list-items")
    if not ul:
        return []

    jobs = []
    for li in ul.find_all("li"):
        wrapper = li.find("div", class_="bjs-jlid__wrapper")
        if not wrapper:
            continue

        company_tag = wrapper.find("a", class_="bjs-jlid__b")
        title_tag = wrapper.find("h4", class_="bjs-jlid__h")

        company = company_tag.get_text(strip=True) if company_tag else ""
        position = title_tag.get_text(strip=True) if title_tag else ""

        link = ""
        if title_tag:
            a = title_tag.find("a")
            if a and a.get("href"):
                link = urljoin(BASE, a["href"])

        if position and link:
            jobs.append(
                {
                    "position": position,
                    "company": company,
                    "link": link,
                    "source": "berlinstartupjobs",
                }
            )

    return jobs