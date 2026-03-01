import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://web3.career"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_web3_jobs(keyword: str) -> list[dict]:
    url = f"{BASE}/{keyword}-jobs"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    jobs = []
    for a in soup.select('a[href^="/jobs/"]'):
        href = a.get("href", "")
        link = urljoin(BASE, href)

        text = a.get_text(" ", strip=True)
        if not text or len(text) < 6:
            continue

        jobs.append(
            {
                "position": text,
                "company": "",
                "link": link,
                "source": "web3.career",
            }
        )

    # 중복 제거(링크 기준)
    seen = set()
    deduped = []
    for j in jobs:
        if j["link"] in seen:
            continue
        seen.add(j["link"])
        deduped.append(j)

    return deduped