import os
import requests
from datetime import datetime

if __name__ == "__main__":
    report = "🧪 这是一条纯文本测试消息\n\nAI硬件趋势监控系统 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n如果看到这条，说明 webhook 基本可用。"

    webhook = os.getenv("LARK_WEBHOOK")
    if webhook:
        payload = {
            "msg_type": "text",
            "content": {"text": report}
        }
        try:
            r = requests.post(webhook, json=payload, timeout=10)
            print("状态码:", r.status_code)
            print("返回:", r.text)
        except Exception as e:
            print("异常:", e)
    else:
        print("未找到 webhook")
