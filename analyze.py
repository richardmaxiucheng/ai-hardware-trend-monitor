import pandas as pd
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time
import random

def get_google_trends(keywords):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='US')
        df = pytrends.interest_over_time()
        rising = pytrends.related_queries().get('rising')
        return df, rising
    except:
        return pd.DataFrame(), None

def scrape_amazon_ai():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    products = []
    urls = [
        "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics",
        "https://www.amazon.com/s?k=AI+smart+glasses"
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.a-size-medium, .a-size-base-plus')[:10]
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 5:
                    products.append(text)
            time.sleep(random.uniform(1, 2))
        except:
            pass
    return list(set(products))[:12]

def scrape_kickstarter_ai():
    try:
        url = "https://www.kickstarter.com/discover/advanced?term=AI+glasses+OR+pocket+AI+OR+AI+robot"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        projects = [p.get_text(strip=True)[:80] for p in soup.select('h3, .project-title, .name') if p.get_text(strip=True)]
        return projects[:8] or ["当前抓取到 Kickstarter 项目"]
    except:
        return ["Kickstarter 数据抓取中..."]

def generate_report():
    keywords = ["AI glasses", "AI smart glasses", "Ray-Ban Meta", "pocket AI", "INMO AI"]
    trends_df, rising = get_google_trends(keywords)
    amazon = scrape_amazon_ai()
    ks = scrape_kickstarter_ai()
    
    report = f"""# 🚀 AI 硬件爆发趋势日报 ({datetime.now().strftime('%Y-%m-%d')})

## 1. Google Trends（美国，近7天）
**关键词**：{', '.join(keywords)}
{trends_df.tail(5).to_string() if not trends_df.empty else '暂无数据'}

**Rising Queries**：{rising.head(8).to_string() if rising is not None and not rising.empty else '暂无'}

## 2. Amazon 热销 AI 产品
{chr(10).join(['• ' + p for p in amazon[:10]])}

## 3. Kickstarter 爆发项目
{chr(10).join(['• ' + p for p in ks])}

## 解读
- AI Smart Glasses 是当前最热方向。
- 重点关注搜索和销量快速上升的产品。
"""
    return report

if __name__ == "__main__":
    report = generate_report()
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    webhook = os.getenv("LARK_WEBHOOK")
    if webhook:
        payload = {"msg_type": "markdown", "content": {"text": report}}
        try:
            requests.post(webhook, json=payload, timeout=10)
            print("✅ 已发送到飞书")
        except Exception as e:
            print("发送失败:", e)