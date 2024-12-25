from flask import Flask
import random
import time
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "order"})
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

@app.route("/")
def order():
    with trace.get_tracer(__name__).start_as_current_span("order"):
        random_order_number = random.randint(1, 500)
        time.sleep(random_order_number * 0.001)  # задержка
        return str(random_order_number)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)