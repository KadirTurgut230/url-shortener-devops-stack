import time
import json
import pika
import psycopg2
from config import settings
from parser import parse_device_type, resolve_country_from_ip

def get_db_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )

def process_click_event(ch, method, properties, body):
    try:
        event = json.loads(body)
        short_code = event.get("short_code")
        ip_address = event.get("ip_address")
        user_agent = event.get("user_agent")

        device_type = parse_device_type(user_agent)
        country = resolve_country_from_ip(ip_address)

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO click_analytics (short_code, country, device_type) 
            VALUES (%s, %s, %s)
            """,
            (short_code, country, device_type)
        )
        conn.commit()
        cursor.close()
        conn.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[OK] Analiz kaydedildi: {short_code} | {country} | {device_type}")

    except Exception as e:
        print(f"[HATA] Mesaj işlenemedi: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_worker():
    print("Analytics Worker başlatılıyor, RabbitMQ bekleniyor...")
    
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ hazır değil, 3 saniye sonra tekrar deneniyor...")
            time.sleep(3)

    channel = connection.channel()
    channel.queue_declare(queue='click_events', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='click_events', on_message_callback=process_click_event)

    print(" [*] Analytics Worker kuyruğu dinlemeye başladı.")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
