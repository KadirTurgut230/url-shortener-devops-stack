import json
import pika
from config import settings

def publish_click_event(short_code: str, ip_address: str, user_agent: str):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue='click_events', durable=True)

        event_data = {
            "short_code": short_code,
            "ip_address": ip_address,
            "user_agent": user_agent
        }

        channel.basic_publish(
            exchange='',
            routing_key='click_events',
            body=json.dumps(event_data)
        )
        connection.close()
    except Exception as e:
        print(f"[HATA] Kuyruğa mesaj gönderilemedi: {e}")
