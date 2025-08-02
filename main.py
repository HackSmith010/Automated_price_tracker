import requests 
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import json
import time
import schedule
import sqlite3

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
DB_FILE = 'price.db'
PRODUCTS_FILE = 'products.json'
CONFIG_FILE = 'sites_config.json'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    url TEXT
                )
                ''')
    conn.commit()
    conn.close()

def save_in_db(date,title,price,url):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO prices (date , title , price , url ) VALUES (?,?,?,?)",
        (date,title,price,url)
    )
    conn.commit()
    conn.close()
    
    print("Successfully Saved data to {DB_FILE}")
    
def track: