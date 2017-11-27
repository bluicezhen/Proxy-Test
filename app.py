from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/verify.php", methods=["GET", "POST", "PUT", "DELETE"])
def verify():
    http_header_keys = []
    for k, _ in request.headers.items():
        http_header_keys.append(k.upper())

    if "HTTP_X_FORWARDED_FOR" in http_header_keys:
        return "transparent"
    if "HTTP_VIA" in http_header_keys:
        return "anonymous"
    else:
        return "elite"


if __name__ == "__main__":
    app.debug = True
    app.run()
