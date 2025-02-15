import random
import time
import ssl

from flask import Flask, request
from prometheus_client import Histogram, make_wsgi_app
from werkzeug import Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app, {"/metrics": make_wsgi_app()}
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration",
    "Requests durations",
    ["method", "url", "code"],
    buckets=[0.01, 0.1, 0.5, 2, float("inf")],
)

def observe_http(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        end = time.time()
        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            code=response.status_code,
            url=request.url,
        ).observe(end - start)
        return response
    return wrapper

@app.route("/")
@app.route("/health")
def check_health():
    return "I am still alive!"

@app.route("/rand_metrics")
@observe_http
def random_metric():
    random_duration = random.randint(1, 50) * 0.001
    time.sleep(random_duration) #задержка
    response_code = random.choice([200, 200, 200, 200, 200, 400, 401, 500]) #коды ответа
    return Response(str(response_code), status=response_code)
