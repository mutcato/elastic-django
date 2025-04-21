# django-api/api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from kombu import Connection, Exchange, Producer

RABBITMQ_URL = "amqp://guest:guest@message-queue:5672//"


class SearchViewSet(viewsets.ModelViewSet):
    def create(self, request):
        data = request.data
        # TODO: Change it with authenticated user
        data["user"] = "anonymous"

        with Connection(RABBITMQ_URL) as conn:
            exchange = Exchange("queries", type="direct")
            producer = Producer(conn)
            producer.publish(
                data, exchange=exchange, routing_key="query_requests", serializer="json"
            )
            print(data)

        return Response(
            {"message": "Query received and sent to queue"}, status=status.HTTP_200_OK
        )
