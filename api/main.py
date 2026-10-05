from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import psycopg2

from utils import generate_short_code
from database import get_db_connection, redis_client
from queue_publisher import publish_click_event

app = FastAPI(title="URL Shortener API")

class URLRequest(BaseModel):
    original_url: HttpUrl

@app.post("/shorten")
def shorten_url(request_data: URLRequest):
    original_url = str(request_data.original_url)
    short_code = generate_short_code()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
            (short_code, original_url)
        )
        conn.commit()
        
        redis_client.set(f"url:{short_code}", original_url)
        
        cursor.close()
        conn.close()
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Veritabanı hatası")

    return {
        "short_code": short_code, 
        "short_url": f"http://localhost/{short_code}"
    }

@app.get("/{short_code}")
def redirect_to_original(short_code: str, request: Request, background_tasks: BackgroundTasks):
    original_url = redis_client.get(f"url:{short_code}")

    if not original_url:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not result:
                raise HTTPException(status_code=404, detail="Link bulunamadı")
            
            original_url = result[0]
            redis_client.set(f"url:{short_code}", original_url)
            
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Veritabanı hatası")

    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    user_agent = request.headers.get("User-Agent", "Unknown")
    
    background_tasks.add_task(publish_click_event, short_code, client_ip, user_agent)

    return RedirectResponse(url=original_url, status_code=302)