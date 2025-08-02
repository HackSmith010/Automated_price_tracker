import requests 
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import json
import time
import schedule
import sqlite3
from urllib.parse import urlparse

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
    
    print(f" > Successfully Saved data for {title[:40]}...")
    
def get_site_config(url,configs):
    domain = urlparse(url).netloc
    
    if domain.startswith('www.'):
        domain = domain[4:]
        
    return configs.get(domain)
        
def track_product(url,config):
    print(f"\n --Tracking : {url[:50]}...")
    response = requests.get(url,headers=HEADERS)
    
    # with open("debug_page.html", "w", encoding="utf-8") as f:
    #     f.write(response.text)  #to get the debug file of the sites

    
    soup = bs(response.content,'html.parser')
    
    try:
        title_config = config['title']
        title = soup.find(title_config['tag'], id=title_config.get('id'), class_=title_config.get('class')).get_text().strip()
        
        price_config = config['price']
        price_str = soup.find(price_config['tag'],id=price_config.get('id'),class_=price_config.get('class')).get_text().strip()
        
        price = float(price_str.replace(",", "").replace('₹', ''))
    except (AttributeError, KeyError):
        print("  > Error: Could not find title or price. Check site config or page layout.")
        return
    
    date = dt.now().strftime("%Y-%m-%d %HH:%MM(:%SS)")
    print(f" > Found {title[:50]}... | Price: ₹{price}")
    save_in_db(date,title,price,url)
    
def job():
    print(f"\n>>> Starting price tracking run at {dt.now().strftime('%Y-%m-%d %HH:%MM(:%SS)')} <<<")
    
    try:
        with open(PRODUCTS_FILE,'r') as f_products ,open(CONFIG_FILE,'r') as f_configs:
            products = json.load(f_products)
            site_configs = json.load(f_configs)
            
            for products in products:
                url = products['url']
                config = get_site_config(url,site_configs)
                
                if config:
                    track_product(url,config)
                else:
                    print(f" > Error: Could not find site config for {url}. Check sites_config.json.")
                    
                time.sleep(5)
    except FileNotFoundError as e:
        print(f" > Error: {str(e)}")
    
if __name__ == '__main__':
    init_db()
    schedule.every().day.at("08:00").do(job)
    
    print("--- Price Tracker with SQLite DB is now running ---")
    
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)         
        