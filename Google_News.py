import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Wikipedia स्क्रैपिंग
def scrape_wikipedia():
    url = "https://en.wikipedia.org/wiki/Category:Media_in_Madhya_Pradesh"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        media_list = [item.text for item in soup.select(".mw-category-group li")]
        return media_list[:50]
    except Exception as e:
        print(f"Wikipedia Error: {e}")
        return []

# JustDial स्क्रैपिंग (Selenium के साथ)
def scrape_justdial():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.justdial.com/Madhya-Pradesh/Newspapers/nct-10292844")
        time.sleep(5)
        
        data = []
        companies = driver.find_elements(By.CSS_SELECTOR, ".resultbox")
        
        for company in companies[:50]:
            try:
                name = company.find_element(By.CSS_SELECTOR, ".resultbox_title").text.strip()
                phone = company.find_element(By.CSS_SELECTOR, ".callcontent").text.strip()
                data.append([name, "Newspaper", phone, "MP"])
            except:
                continue
                
        return data
    except Exception as e:
        print(f"JustDial Error: {e}")
        return []
    finally:
        driver.quit()

# Google News API
def google_news_mp():
    api_key = "Your API Key"  # यहाँ अपना API key डालें
    url = f"https://newsapi.org/v2/everything?q=Madhya+Pradesh&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_sources = []
        
        for article in response.json().get('articles', [])[:50]:
            news_sources.append([
                article['source']['name'],
                "News Portal",
                article.get('url', 'N/A'),
                "MP"
            ])
        return news_sources
    except Exception as e:
        print(f"News API Error: {e}")
        return []

# एक्सेल में सेव करें
def save_to_excel():
    wikipedia_data = [[item, "Unknown", "", "MP"] for item in scrape_wikipedia()]
    justdial_data = scrape_justdial()
    google_news_data = google_news_mp()
    
    all_data = wikipedia_data + justdial_data + google_news_data
    df = pd.DataFrame(all_data, columns=["Media Name", "Type", "Contact/URL", "City"])
    
    print(f"कुल डेटा एंट्रीज: {len(all_data)}")
    print(df.head())
    
    df.to_excel("mp_media_dynamic.xlsx", index=False)
    print("एक्सेल फाइल सेव हुई: mp_media_dynamic.xlsx")

save_to_excel()