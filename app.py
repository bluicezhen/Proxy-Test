import logging
from flask import Flask, render_template, request

app = Flask(__name__)


def get_logger(level: int = logging.DEBUG, stream_out: bool = True, file_path: str = None) -> logging.Logger:
    """ Get My Logger Function
    Copy from https://gist.github.com/bluicezhen/2e43035a52fd1be77669ed27a38d4b32

    :param level:       Log level.
    :param stream_out:  Weather write log to stream.
    :param file_path:   File path to  write log to. If none, no log file
    :return: Logger object
    """
    logger = logging.Logger(__name__)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)7s: %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    if stream_out:
        sh = logging.StreamHandler(stream=None)
        sh.setLevel(level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    if file_path:
        fh = logging.FileHandler(file_path, mode='a', encoding="utf-8", delay=False)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/verify.php", methods=["GET", "POST", "PUT", "DELETE"])
def verify():
    logger = get_logger(stream_out=False, file_path="proxy_test.log")
    http_header_keys = []

    for k, _ in request.headers.items():
        http_header_keys.append(k.upper())

    proxy_type = "elite"
    if "HTTP_X_FORWARDED_FOR" in http_header_keys:
        proxy_type = "transparent"
    if "HTTP_VIA" in http_header_keys:
        proxy_type = "anonymous"

    logger.info(f"Proxy IP: { request.remote_addr.ljust(16) }"
                f"Type: { proxy_type.ljust(12) }"
                f"Client UA: { request.headers.get('user-agent') }")

    return proxy_type


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
