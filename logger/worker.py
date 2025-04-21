from kombu import Connection, Exchange, Queue, Consumer
import json
import time

RABBITMQ_URL = "amqp://guest:guest@message-queue:5672//"

exchange = Exchange("logs", type="direct")
queue = Queue(
    "log_events",
    exchange=exchange,
    routing_key="log_events",
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


def log_event(body, message):
    print(f"[logger] Logging: {body}")
    with open("/app/query_logs.txt", "a") as log_file:
        log_file.write(json.dumps(body) + "\n")
    message.ack()


def run():
    with Connection(RABBITMQ_URL) as conn:
        with conn.channel() as channel:
            queue.maybe_bind(conn)
            queue.declare()
            with Consumer(
                channel, queues=[queue], callbacks=[log_event], accept=["json"]
            ):
                print("[logger] Waiting for logs...")
                while True:
                    print("START DRAINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
                    conn.drain_events()


if __name__ == "__main__":
    run()
