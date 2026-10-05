-- 1. URL Eşleşme Tablosu
CREATE TABLE IF NOT EXISTS urls (
    short_code VARCHAR(10) PRIMARY KEY,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tıklama Analiz Tablosu
CREATE TABLE IF NOT EXISTS click_analytics (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(10) NOT NULL REFERENCES urls(short_code) ON DELETE CASCADE,
    country VARCHAR(50),
    device_type VARCHAR(20),
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);