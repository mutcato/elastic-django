from kombu import Connection, Exchange, Queue, Consumer
import time


RABBITMQ_URL = "amqp://guest:guest@message-queue:5672//"

# Define the exchange and queue names used by the API service
exchange = Exchange("queries", type="direct")
queue = Queue(
    "query_requests",
    exchange=exchange,
    routing_key="query_requests",
    durable=True,
    auto_delete=False,
    auto_declare=True,
)


def wait_for_rabbitmq():
    while True:
        try:
            conn = Connection(RABBITMQ_URL)
            conn.connect()
            print("[Logger] Connected to RabbitMQ!")
            conn.release()
            break
        except Exception as e:
            print(f"[Logger] Waiting for RabbitMQ... ({e})")
            time.sleep(3)


wait_for_rabbitmq()


def handle_query_request(body, message):
    print(f"[Converter] Received query: {body}")

    # TODO: Convert query to Elasticsearch DSL
    # TODO: Send converted query to Elasticsearch
    # TODO: Forward to logger service if needed

    # Acknowledge message
    message.ack()


def run_worker():
    print(123456711)
    print("[Converter] Worker started and waiting for messages...")

    with Connection(RABBITMQ_URL) as conn:
        with conn.channel() as channel:
            print("[Converter] Declaring and binding queue...")
            queue.maybe_bind(conn)
            queue.declare()
            print("[Converter] Queue declared.")

            with Consumer(
                channel, queues=queue, callbacks=[handle_query_request], accept=["json"]
            ):
                while True:
                    try:
                        print("FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                        print("START DRAINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN CONVERTER")
                        conn.drain_events(timeout=10)
                    except Exception:
                        print("[Converter] Error while processing message.")
                        # TODO: Logger


if __name__ == "__main__":
    run_worker()
