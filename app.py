from flask import Flask, request, send_from_directory, Response
from flask import render_template
from tinydb import TinyDB, Query
import json, threading
import logging, datetime
import webbrowser, requests
from logging.config import dictConfig
from flask_cors import CORS

format = "%(asctime)-15s - %(levelname)-7s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=format)
logger = logging.getLogger("app")
app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="templates/build/static",
)
from flask.logging import default_handler

CORS(app)

# logger = app.logger
# format = "%(asctime)-15s - %(levelname)-7s - %(message)s"
# logging.basicConfig(level=logging.DEBUG, format=format)
url = "https://api.bseindia.com:443/BseIndiaAPI/api/AnnGetData/w"
req_ids = [543271, 539276]


db = TinyDB("database.json")
query = Query()


@app.route("/")
def hello_world(name=None):
    return render_template("build/index.html", name=name)


@app.route("/bse/news/data")
def send_js():
    return Response(json.dumps(db.all()), mimetype="application/json")


@app.route("/bse/news/updates")
def get_data():
    now = datetime.datetime.now()
    date1 = datetime.datetime.strftime(now, "%Y%m%d")
    querystring = {
        "strCat": "-1",
        "strPrevDate": date1,
        "strScrip": "",
        "strSearch": "P",
        "strToDate": date1,
        "strType": "C",
    }

    headers = {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    }

    logger.info("Connecting to bseindia API")
    logger.debug(url)
    response = requests.request("GET", url, headers=headers, params=querystring)
    status = response.status_code
    logger.info(f"API response - {status}")

    if status == 200:
        data = json.loads(response.text)
        count = len(data["Table"])
        logger.info(f"No of News fetched - {count}")
        logger.debug(f"Parsing response data to database")
        for item in data["Table"]:
            if len(req_ids) < 10:
                req_ids.append(item["SCRIP_CD"])
            company_id = item["SCRIP_CD"]

            item["date"] = datetime.datetime.strftime(now, "%d-%m-%Y")
            if company_id in req_ids and not db.search(query.NEWSID == item["NEWSID"]):
                db.insert(item)
        return Response(json.dumps(db.all()), mimetype="application/json")
    else:
        raise Exception("Connection error.. Try again")


if __name__ == "__main__":
    threading.Timer(1.25, lambda: webbrowser.open_new("http://127.0.0.1:5000/")).start()
    app.run(debug=True, port=5000, host="127.0.0.1")
