from flask import Flask, session, render_template, request
import google
import urllib

app = Flask(__name__)


def switchboard(s):
    
    
    return "who"

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        query = request.form['query']
        g = google.search("query", num = 100, start = 0, stop = 100)
        s = switchboard(s)

    


if __name__ == "__main__":
    app.debug = True
    app.run()
