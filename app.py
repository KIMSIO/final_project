from flask import Flask, render_template, request
from flask_frozen import Freezer

from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs

app = Flask(__name__)
freezer = Freezer(app)

db = {}  # cache


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search_page():
    keyword = request.args.get("keyword", "").strip().lower()

    if keyword == "":
        return render_template("results.html", keyword=keyword, jobs=[], error="Please write a keyword.")

    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = []
        jobs += extract_berlin_jobs(keyword)
        jobs += extract_web3_jobs(keyword)

        seen = set()
        deduped = []
        for j in jobs:
            if j["link"] in seen:
                continue
            seen.add(j["link"])
            deduped.append(j)

        db[keyword] = deduped
        jobs = deduped

    return render_template("results.html", keyword=keyword, jobs=jobs, error=None)


# Frozen-Flask: /search 페이지를 키워드별로 미리 생성
@freezer.register_generator("search_page")
def search_generator():
    for keyword in ["python", "javascript", "java"]:
        yield {"keyword": keyword}

        
if __name__ == "__main__":
    freezer.freeze()