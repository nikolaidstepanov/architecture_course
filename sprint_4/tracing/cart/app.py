from flask import Flask
import requests
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "cart"})
    )
)

try:
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",  # Ensure this hostname is correct and reachable
        agent_port=6831,
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
except Exception as e:
    logger.error(f"Failed to configure Jaeger exporter: {e}")

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/buy")
def buy():
    with trace.get_tracer(__name__).start_as_current_span("buy"):
        res = requests.get("http://billing:8000")
        return res.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)