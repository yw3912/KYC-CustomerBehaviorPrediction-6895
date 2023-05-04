from flask import Flask, Response, request
from multiprocessing import Process, Pipe

from flask_cors import CORS

import evaluation_scrape


# Create the Flask application object.
app = Flask(__name__)

CORS(app)



def calculate(pipe, url):
    creativity = evaluation_scrape.get_info_by_link(url)
    pipe.send(creativity)
    pipe.close()


@app.route("/api/review/<path:link>", methods=["GET"])
def get_info(link):
    ie = request.args.get("ie")
    ASIN = request.args.get("ASIN")
    combine_link = link + "?ie=" + ie + "&ASIN="+ASIN

    parent_conn, child_conn = Pipe()
    p = Process(target=calculate, args=(child_conn, combine_link))
    p.start()
    creativity = parent_conn.recv()[0]
    creativity = str(creativity)
    p.join()

    result = "{"+f"\"link\": \"{combine_link}\", \"creativity\": \"{creativity}\""+"}"
    return Response(result, status=200, content_type="application.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
